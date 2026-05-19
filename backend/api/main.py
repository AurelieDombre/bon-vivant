"""
Point d'entree HTTP du backend.

Ce fichier declare l'application FastAPI et les routes exposees au frontend.
Le flux principal est le suivant :

1. Le frontend envoie un message a /chat
2. On regarde d'abord si le message correspond a un produit connu
3. Si oui, on repond avec la logique metier locale
4. Sinon, on delegue la reponse a Ollama

Ce fichier contient aussi les routes d'analyse d'image :
- une route qui recoit un vrai fichier image
- une route qui recoit simplement un chemin deja present sur le disque
"""

import os
import tempfile

from fastapi import FastAPI, UploadFile, File
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import ChatRequest, ChatResponse, ImageRequest, ImageResponse
from core.llm_client import LLMClient
from core.services import analyze_sentiment, get_product_info
from core.vision_client import analyze_image

# Liste des origines autorisees a appeler l'API depuis le navigateur.
# Ici on autorise le serveur Vite local du frontend.
origins = [
    "http://localhost:5173",
]

# Creation de l'application FastAPI.
app = FastAPI()

# Ajout du middleware CORS.
# Sans lui, le navigateur bloquerait les appels du frontend React vers l'API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instance unique du client LLM.
# On la cree une seule fois au demarrage pour la reutiliser ensuite.
llm_client = LLMClient()


@app.get("/")
def home():
    """
    Route de test simple.

    Elle permet de verifier rapidement que l'API repond.
    """
    return {
        "message": "API chatbot OK"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Route principale du chatbot.

    Entree :
    - request.user_message : texte tape par l'utilisateur

    Sortie :
    - un objet ChatResponse contenant une recommandation

    Strategie :
    - on tente d'abord la logique locale basee sur les produits du JSON
    - si rien n'est trouve, on construit un prompt pour Ollama
    """

    # On essaie d'abord de repondre avec les regles metier locales.
    # Exemple : "Je veux du brie" => reponse basee sur products.json.
    service_response = get_product_info(request.user_message)

    if service_response:
        recommendation = service_response
    else:
        # L'appel a Ollama est bloquant.
        # run_in_threadpool permet de ne pas bloquer la boucle asynchrone
        # de FastAPI pendant l'execution du modele.
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

    # Analyse de sentiment du message utilisateur.
    # On recupere :
    # - un label : positive / negative / neutral
    # - un score de confiance du modele
    sentiment, score = analyze_sentiment(request.user_message)

    # Regle metier d'escalade :
    # si le message est detecte comme negatif avec une confiance elevee,
    # on indique qu'un humain devrait potentiellement reprendre la main.
    escalate = (sentiment == "negative" and score > 0.75)

    # Logs simples visibles dans le terminal du backend.
    # C'est pratique pendant l'apprentissage pour observer le comportement.
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

    Cette route est utile quand on envoie un vrai fichier .jpg
    en multipart/form-data depuis un formulaire ou un outil de test.
    """
    # On lit d'abord le contenu binaire du fichier envoye.
    content = await file.read()

    # On cree un fichier temporaire compatible avec Windows et Linux.
    # C'est plus robuste qu'un chemin fixe comme /tmp/...
    suffix = os.path.splitext(file.filename or "")[1] or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(content)
        path = temp_file.name

    try:
        # Le client vision attend un chemin local vers l'image.
        desc = analyze_image(path)
        return {"description": desc}
    finally:
        # On supprime le fichier temporaire apres usage pour garder
        # un disque propre.
        if os.path.exists(path):
            os.remove(path)

@app.post("/image/analyze", response_model=ImageResponse)
async def analyze_image_endpoint(request: ImageRequest):
    """
    Analyse une image deja presente sur le disque.

    Cette route est pratique pour les tests du cours :
    on met une image dans le dossier tests puis on envoie son chemin absolu.
    """
    description = analyze_image(request.image_path)
    return ImageResponse(description=description)
