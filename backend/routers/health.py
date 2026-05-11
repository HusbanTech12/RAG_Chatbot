from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.dependencies import get_vector_store, get_embedding_service
from services.rag.vector_store import VectorStore
from services.rag.embeddings import EmbeddingService

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check(
    db: AsyncSession = Depends(get_db),
    vector_store: VectorStore = Depends(get_vector_store),
    embedding_service: EmbeddingService = Depends(get_embedding_service)
):
    """
    Health check endpoint.

    Checks the status of database, vector store, and embedding service.
    """
    status = {
        "status": "healthy",
        "services": {}
    }

    # Check database
    try:
        await db.execute("SELECT 1")
        status["services"]["database"] = "healthy"
    except Exception as e:
        status["services"]["database"] = f"unhealthy: {str(e)}"
        status["status"] = "unhealthy"

    # Check vector store
    try:
        # Simple check - see if collection exists
        collection = vector_store.collection
        status["services"]["vector_store"] = "healthy"
    except Exception as e:
        status["services"]["vector_store"] = f"unhealthy: {str(e)}"
        status["status"] = "unhealthy"

    # Check embedding service
    try:
        # Simple check - service is initialized
        if embedding_service.client:
            status["services"]["embedding_service"] = "healthy"
        else:
            status["services"]["embedding_service"] = "unhealthy: client not initialized"
            status["status"] = "unhealthy"
    except Exception as e:
        status["services"]["embedding_service"] = f"unhealthy: {str(e)}"
        status["status"] = "unhealthy"

    return status
