from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns basic health status without initializing heavy services.
    """
    return {
        "status": "healthy",
        "message": "RAG Chatbot API is running"
    }
