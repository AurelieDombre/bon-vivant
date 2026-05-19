from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import ChatRequest, ChatResponse
from core.llm_client import LLMClient
from core.services import get_product_info

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

# Instance du client IA
llm_client = LLMClient()


@app.get("/")
def home():
    return {
        "message": "API chatbot OK"
    }


# Endpoint chatbot
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    service_response = get_product_info(request.user_message)
    if service_response:
        return ChatResponse(recommendation=service_response)

    prompt = (
        "Tu es un assistant qui recommande des accords mets et vins. "
        "Réponds en français de façon concise et utile. "
        f"Question utilisateur : {request.user_message}"
    )

    response = llm_client.complete(prompt)

    # Retour API
    return ChatResponse(
        recommendation=response
    )
