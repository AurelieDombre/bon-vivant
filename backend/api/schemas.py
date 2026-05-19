"""
Schemas Pydantic utilises par l'API.

Un schema sert a definir clairement :
- ce que l'API attend en entree
- ce qu'elle renvoie en sortie

FastAPI s'appuie dessus pour :
- valider les donnees recues
- documenter automatiquement l'API dans /docs
"""

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
    # Sentiment detecte sur le message utilisateur.
    sentiment: str

    # Indique si le message doit etre remonte a un humain.
    escalate_to_human: bool
