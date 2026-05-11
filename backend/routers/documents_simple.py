from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List
import uuid

from core.dependencies import (
    get_document_chunker,
    get_embedding_service,
    get_vector_store
)
from services.rag.chunking import DocumentChunker
from services.rag.embeddings_hf import HuggingFaceEmbeddingService
from services.rag.vector_store import VectorStore

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    chunker: DocumentChunker = Depends(get_document_chunker),
    embedding_service: HuggingFaceEmbeddingService = Depends(get_embedding_service),
    vector_store: VectorStore = Depends(get_vector_store)
):
    """
    Upload and process a document for RAG.

    Simplified version without database persistence.
    """
    try:
        # Read file content
        content = await file.read()
        text = content.decode('utf-8')

        # Chunk the document
        chunks = chunker.chunk_text(text)

        if not chunks:
            raise HTTPException(status_code=400, detail="No content to process")

        # Generate embeddings for all chunks
        texts = [chunk['text'] for chunk in chunks]
        embeddings = []
        for text in texts:
            embedding = await embedding_service.embed(text)
            embeddings.append(embedding)

        # Generate IDs and metadata
        document_id = str(uuid.uuid4())
        ids = [f"{document_id}_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "document_id": document_id,
                "filename": file.filename,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            for i in range(len(chunks))
        ]

        # Store in vector database
        await vector_store.add_documents(
            texts=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        return {
            "document_id": document_id,
            "filename": file.filename,
            "chunks_created": len(chunks),
            "message": "Document uploaded and processed successfully"
        }

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must be a text file (UTF-8 encoded)"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )


@router.get("/test")
async def test_documents():
    """Test endpoint to verify documents router is working."""
    return {
        "status": "ok",
        "message": "Documents router is working"
    }
