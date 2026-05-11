from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


class DocumentUpload(BaseModel):
    """Request model for document upload."""
    filename: str = Field(..., description="Document filename")
    content_type: str = Field(..., description="Document content type")


class DocumentResponse(BaseModel):
    """Response model for document upload."""
    document_id: str = Field(..., description="Document ID")
    filename: str = Field(..., description="Document filename")
    chunks_created: int = Field(..., description="Number of chunks created")
    message: str = Field(..., description="Success message")


class DocumentInfo(BaseModel):
    """Document information model."""
    id: str
    filename: str
    uploaded_at: datetime
    chunk_count: int
    metadata: Dict = Field(default_factory=dict)


class DocumentList(BaseModel):
    """Response model for listing documents."""
    documents: list[DocumentInfo]
    total: int
