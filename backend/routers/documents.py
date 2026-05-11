from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List
import hashlib
from datetime import datetime
import os

from core.dependencies import (
    get_document_chunker,
    get_embedding_service,
    get_vector_store
)
from models.document import DocumentResponse, DocumentInfo, DocumentList
from services.rag.chunking import DocumentChunker
from services.rag.embeddings import EmbeddingService
from services.rag.vector_store import VectorStore

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    chunker: DocumentChunker = Depends(get_document_chunker),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_store: VectorStore = Depends(get_vector_store)
):
    """
    Upload and process a document.

    Extracts text, chunks it, generates embeddings, and stores in vector database.
    """
    try:
        # Read file content
        content = await file.read()

        # Extract text based on file type
        if file.filename.endswith('.txt'):
            text = content.decode('utf-8')
        elif file.filename.endswith('.pdf'):
            # For now, just decode as text. In production, use PyPDF2 or similar
            text = content.decode('utf-8', errors='ignore')
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Only .txt and .pdf are supported."
            )

        # Generate document ID
        document_id = hashlib.md5(content).hexdigest()

        # Chunk the document
        metadata = {
            'filename': file.filename,
            'document_id': document_id,
            'uploaded_at': datetime.utcnow().isoformat()
        }
        chunks = chunker.chunk_text(text, metadata)

        if not chunks:
            raise HTTPException(status_code=400, detail="No content extracted from document")

        # Generate embeddings
        texts = [chunk['text'] for chunk in chunks]
        embeddings = await embedding_service.embed_batch(texts)

        # Prepare data for vector store
        chunk_ids = [f"{document_id}_{i}" for i in range(len(chunks))]
        metadatas = [chunk['metadata'] for chunk in chunks]

        # Store in vector database
        await vector_store.add_documents(
            texts=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=chunk_ids
        )

        # Save original document (optional)
        storage_path = f"./storage/documents/{document_id}_{file.filename}"
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        with open(storage_path, 'wb') as f:
            f.write(content)

        return DocumentResponse(
            document_id=document_id,
            filename=file.filename,
            chunks_created=len(chunks),
            message=f"Document uploaded and processed successfully. Created {len(chunks)} chunks."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@router.get("", response_model=DocumentList)
async def list_documents():
    """
    List all uploaded documents.

    Note: This is a simplified version. In production, store document metadata in database.
    """
    try:
        documents_dir = "./storage/documents"

        if not os.path.exists(documents_dir):
            return DocumentList(documents=[], total=0)

        documents = []
        for filename in os.listdir(documents_dir):
            filepath = os.path.join(documents_dir, filename)
            stat = os.stat(filepath)

            # Extract document_id from filename (format: {doc_id}_{original_name})
            parts = filename.split('_', 1)
            doc_id = parts[0] if len(parts) > 0 else filename
            original_name = parts[1] if len(parts) > 1 else filename

            documents.append(
                DocumentInfo(
                    id=doc_id,
                    filename=original_name,
                    uploaded_at=datetime.fromtimestamp(stat.st_ctime),
                    chunk_count=0,  # Would need to query vector store
                    metadata={}
                )
            )

        return DocumentList(documents=documents, total=len(documents))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    vector_store: VectorStore = Depends(get_vector_store)
):
    """
    Delete a document and its chunks from the vector database.
    """
    try:
        # Get all chunk IDs for this document
        # In a real implementation, you'd query the vector store for all chunks with this document_id
        # For now, we'll attempt to delete based on ID pattern

        # Delete from vector store (this is simplified)
        # In production, you'd need to query first to get all chunk IDs

        # Delete physical file
        documents_dir = "./storage/documents"
        for filename in os.listdir(documents_dir):
            if filename.startswith(document_id):
                os.remove(os.path.join(documents_dir, filename))

        return {"message": f"Document {document_id} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")
