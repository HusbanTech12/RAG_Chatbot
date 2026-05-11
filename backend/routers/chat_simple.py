from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from typing import List, Dict
import json

from core.dependencies import get_rag_pipeline
from services.rag.pipeline_hf import HuggingFaceRAGPipeline
from models.chat_simple import ChatRequest

router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.post("/chat")
async def chat_simple(
    request: ChatRequest,
    rag_pipeline: HuggingFaceRAGPipeline = Depends(get_rag_pipeline)
):
    """
    Simplified chat endpoint using Hugging Face (Free).

    No conversation history or persistence - just RAG-based responses.
    """
    async def generate():
        try:
            # Generate response without conversation history
            async for chunk in rag_pipeline.generate_response(
                query=request.query,
                conversation_history=[],
                n_results=request.n_results or 5
            ):
                yield f"data: {json.dumps(chunk)}\n\n"
        except Exception as e:
            error_chunk = {
                'error': str(e),
                'done': True
            }
            yield f"data: {json.dumps(error_chunk)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@router.get("/test")
async def test_endpoint():
    """Simple test endpoint to verify router is working."""
    return {
        "status": "ok",
        "message": "Chat router is working with Hugging Face (Free)",
        "note": "Get your free API key at https://huggingface.co/settings/tokens"
    }
