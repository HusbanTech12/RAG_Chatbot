from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
import uuid


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    query: str = Field(..., description="User query")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    n_results: int = Field(5, description="Number of documents to retrieve", ge=1, le=20)


class Source(BaseModel):
    """Source document information."""
    text: str = Field(..., description="Document text preview")
    metadata: Dict = Field(default_factory=dict, description="Document metadata")
    score: float = Field(..., description="Relevance score")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="Generated response")
    conversation_id: str = Field(..., description="Conversation ID")
    sources: List[Source] = Field(default_factory=list, description="Source documents")


class MessageModel(BaseModel):
    """Message model."""
    id: str
    role: str = Field(..., description="Message role (user or assistant)")
    content: str = Field(..., description="Message content")
    created_at: datetime


class ConversationModel(BaseModel):
    """Conversation model."""
    id: str
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    messages: List[MessageModel] = Field(default_factory=list)

    class Config:
        from_attributes = True


class ConversationCreate(BaseModel):
    """Request model for creating a conversation."""
    title: Optional[str] = Field(None, description="Conversation title")


class ConversationList(BaseModel):
    """Response model for listing conversations."""
    conversations: List[ConversationModel]
    total: int
