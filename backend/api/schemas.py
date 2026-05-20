"""
Schemas Pydantic utilises par l'API.

Pydantic garantit :
- la structure des données,
- la validation automatique,
- des échanges frontend/backend fiables.

Un schema sert a definir clairement :
- ce que l'API attend en entree
- ce qu'elle renvoie en sortie

FastAPI s'appuie dessus pour :
- valider les donnees recues
- documenter automatiquement l'API dans /docs
"""

from typing import List

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """
    Corps JSON attendu par la route POST /chat.

    Exemple:
    {
        "user_message": "Je veux du brie"
    }
    """

    user_message: str


class ChatResponse(BaseModel):
    """
    Corps JSON renvoye par la route POST /chat.

    Exemple:
    {
        "recommendation": "Pour Brie, je te recommande...",
        "sentiment": "neutral",
        "escalate_to_human": false
    }
    """

    recommendation: str
    sentiment: str
    escalate_to_human: bool


class ImageRequest(BaseModel):
    """
    Corps JSON attendu par la route POST /image/analyze.

    Exemple:
    {
        "image_path": "C:\\mon-projet\\tests\\photo.jpg"
    }
    """

    image_path: str


class ImageResponse(BaseModel):
    """
    Corps JSON renvoye apres analyse d'une image.

    Exemple:
    {
        "description": "On voit une bouteille de vin sur une table..."
    }
    """

    description: str


class VoiceResponse(BaseModel):
    """
    Corps JSON renvoye par la route POST /voice-chat.

    Exemple:
    {
        "transcript": "bonjour",
        "ai_answer": "Je te conseille un vin blanc...",
        "audio_filename": "reponse.wav",
        "audio_url": "/voice-audio/reponse.wav"
    }
    """

    transcript: str
    ai_answer: str
    audio_filename: str | None = None
    audio_url: str | None = None


class UpsellRequest(BaseModel):
    """
    Corps JSON attendu par la route POST /upsell.

    Exemple:
    {
        "cart_items": ["Brunch Estival", "Pinot Noir"]
    }
    """

    cart_items: List[str]


class UpsellResponse(BaseModel):
    """
    Corps JSON renvoye par la route POST /upsell.

    Exemple:
    {
        "suggestion": "Fromage de Chevre"
    }
    """

    suggestion: str
