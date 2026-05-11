from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    """Chat request model."""
    query: str
    conversation_id: Optional[str] = None
    n_results: Optional[int] = 5
