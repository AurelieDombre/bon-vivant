"""
Point d'entree HTTP du backend.

Ce fichier declare l'application FastAPI et les routes exposees au frontend.
Le flux principal est le suivant :

1. Le frontend envoie un message a /chat
2. On regarde d'abord si le message correspond a un produit connu
3. Si oui, on repond avec la logique metier locale
4. Sinon, on delegue la reponse a Ollama

Ce fichier contient aussi :
- des routes d'analyse d'image
- une route de chat vocal basee sur un fichier audio envoye par le client
"""

import os
import tempfile

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from api.schemas import (
    ChatRequest,
    ChatResponse,
    ImageRequest,
    ImageResponse,
    VoiceResponse,
)
from core.llm_client import LLMClient
from core.services import analyze_sentiment, get_product_info
from core.vision_client import analyze_image
from core.voice_service import USE_DEMO_VOICE, speak_text, transcribe_audio


origins = [
    "http://localhost:5173",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_client = LLMClient()


@app.get("/")
def home():
    """
    Route de test simple.
    """
    return {"message": "API chatbot OK"}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Route principale du chatbot texte.
    """
    service_response = get_product_info(request.user_message)

    if service_response:
        recommendation = service_response
    else:
        prompt = (
            "Tu es un assistant qui recommande des accords mets et vins. "
            "Reponds uniquement en francais. "
            f"L'utilisateur demande : {request.user_message}. "
            "Que recommandes-tu comme vin ?"
        )

        recommendation = await run_in_threadpool(
            llm_client.complete,
            prompt
        )

    sentiment, score = analyze_sentiment(request.user_message)
    escalate = (sentiment == "negative" and score > 0.75)

    if escalate:
        print(
            f'[ESCALADE] Message critique detecte : '
            f'"{request.user_message}" '
            f'(sentiment : {sentiment}, score : {score})'
        )
    else:
        print(
            f'[INFO] Message traite : '
            f'"{request.user_message}" '
            f'(sentiment : {sentiment}, score : {score})'
        )

    return ChatResponse(
        recommendation=recommendation,
        sentiment=sentiment,
        escalate_to_human=escalate
    )


@app.post("/chat/photo")
async def chat_photo(file: UploadFile = File(...)):
    """
    Recoit une image envoyee directement par le client puis la fait analyser.
    """
    content = await file.read()

    suffix = os.path.splitext(file.filename or "")[1] or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(content)
        path = temp_file.name

    try:
        desc = analyze_image(path)
        return {"description": desc}
    finally:
        if os.path.exists(path):
            os.remove(path)


@app.post("/image/analyze", response_model=ImageResponse)
async def analyze_image_endpoint(request: ImageRequest):
    """
    Analyse une image deja presente sur le disque.
    """
    description = analyze_image(request.image_path)
    return ImageResponse(description=description)


@app.post("/voice-chat", response_model=VoiceResponse)
async def voice_chat(
    background_tasks: BackgroundTasks,
    audio: UploadFile = File(...),
):
    """
    Recoit un fichier audio, le transcrit, envoie le texte au chatbot
    puis genere un fichier de reponse audio.

    Limite importante actuelle :
    - la transcription supporte les fichiers WAV
    - un .ogg ne peut pas etre traite tel quel sans conversion
    """
    if USE_DEMO_VOICE:
        demo_transcript = "Bonjour, ceci est une transcription simulee."
        demo_ai_answer = "Voici une reponse IA simulee par le mode demo."
        demo_audio_filename = "demo.wav"
        demo_path = os.path.join(tempfile.gettempdir(), demo_audio_filename)

        with open(demo_path, "wb") as f:
            f.write(b"\x00\x00")

        return VoiceResponse(
            transcript=demo_transcript,
            ai_answer=demo_ai_answer,
            audio_filename=demo_audio_filename,
            audio_url=f"/voice-audio/{demo_audio_filename}"
        )

    # On garde l'extension du fichier envoye pour pouvoir signaler
    # clairement les formats non pris en charge.
    suffix = os.path.splitext(audio.filename or "")[1].lower()

    if suffix != ".wav":
        raise HTTPException(
            status_code=400,
            detail=(
                "Le pipeline voix actuel attend un fichier .wav. "
                "Le fichier recu est en format "
                f"'{suffix or 'inconnu'}'. "
                "Ton .ogg doit etre converti en .wav avant transcription."
            ),
        )

    temp_in = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    content = await audio.read()
    temp_in.write(content)
    temp_in.flush()
    temp_in.close()

    try:
        transcribed_text = transcribe_audio(temp_in.name)

        prompt = (
            f"L'utilisateur dit : {transcribed_text}. "
            "Reponds uniquement en francais. "
            "Que recommandes-tu comme vin ?"
        )
        ai_response = await run_in_threadpool(llm_client.complete, prompt)

        temp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_out.close()

        speak_text(ai_response, temp_out.name)

        background_tasks.add_task(os.remove, temp_in.name)

        filename = os.path.basename(temp_out.name)
        return VoiceResponse(
            transcript=transcribed_text,
            ai_answer=ai_response,
            audio_filename=filename,
            audio_url=f"/voice-audio/{filename}"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant le traitement vocal : {exc}"
        ) from exc


@app.get("/voice-audio/{filename}")
async def get_voice_audio(filename: str):
    """
    Sert un fichier audio genere par la route /voice-chat.
    """
    path = os.path.join(tempfile.gettempdir(), filename)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Fichier audio introuvable.")

    return FileResponse(path, media_type="audio/wav", filename=filename)
