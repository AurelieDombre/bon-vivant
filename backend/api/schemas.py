#créé les schemas Pydantic

from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_message: str


class ChatResponse(BaseModel):
    recommendation: str