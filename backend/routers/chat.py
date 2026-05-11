from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import json
import uuid

from core.database import get_db
from core.dependencies import (
    get_rag_pipeline,
    get_conversation_memory,
    get_query_rewriter
)
from models.chat import (
    ChatRequest,
    ConversationModel,
    ConversationCreate,
    ConversationList,
    MessageModel
)
from services.rag.pipeline import RAGPipeline
from services.conversation.memory import ConversationMemory
from services.conversation.query_rewriter import QueryRewriter

router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.post("/chat")
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    rag_pipeline: RAGPipeline = Depends(get_rag_pipeline),
    conversation_memory: ConversationMemory = Depends(get_conversation_memory),
    query_rewriter: QueryRewriter = Depends(get_query_rewriter)
):
    """
    Chat endpoint with streaming response.

    Handles conversation context, query rewriting, and RAG-based response generation.
    """
    try:
        # Get or create conversation
        if request.conversation_id:
            conversation_id = uuid.UUID(request.conversation_id)
            conversation = await conversation_memory.get_conversation(db, conversation_id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = await conversation_memory.create_conversation(db)
            conversation_id = conversation.id

        # Get conversation history
        history = await conversation_memory.get_recent_messages(db, conversation_id, n=10)

        # Rewrite query with context if there's history
        query = request.query
        if history:
            query = await query_rewriter.rewrite_with_context(request.query, history)

        # Save user message
        await conversation_memory.add_message(
            db,
            conversation_id,
            role="user",
            content=request.query
        )

        # Generate streaming response
        async def generate():
            full_response = ""
            sources = []

            async for chunk in rag_pipeline.generate_response(
                query=query,
                conversation_history=history,
                n_results=request.n_results
            ):
                if chunk.get('done'):
                    # Save assistant message
                    await conversation_memory.add_message(
                        db,
                        conversation_id,
                        role="assistant",
                        content=full_response
                    )

                    # Send final chunk with metadata
                    final_data = {
                        'token': '',
                        'done': True,
                        'conversation_id': str(conversation_id),
                        'sources': chunk.get('sources', [])
                    }
                    yield f"data: {json.dumps(final_data)}\n\n"
                else:
                    # Stream token
                    token = chunk.get('token', '')
                    full_response += token
                    yield f"data: {json.dumps({'token': token, 'done': False})}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations", response_model=ConversationList)
async def list_conversations(
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    conversation_memory: ConversationMemory = Depends(get_conversation_memory)
):
    """List all conversations."""
    conversations = await conversation_memory.list_conversations(db, limit, offset)

    conversation_models = []
    for conv in conversations:
        messages = await conversation_memory.get_conversation_history(db, conv.id, limit=10)
        conversation_models.append(
            ConversationModel(
                id=str(conv.id),
                title=conv.title,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                messages=[
                    MessageModel(
                        id=str(msg.id),
                        role=msg.role,
                        content=msg.content,
                        created_at=msg.created_at
                    )
                    for msg in messages
                ]
            )
        )

    return ConversationList(
        conversations=conversation_models,
        total=len(conversation_models)
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationModel)
async def get_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
    conversation_memory: ConversationMemory = Depends(get_conversation_memory)
):
    """Get a specific conversation with all messages."""
    try:
        conv_id = uuid.UUID(conversation_id)
        conversation = await conversation_memory.get_conversation(db, conv_id)

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        messages = await conversation_memory.get_conversation_history(db, conv_id)

        return ConversationModel(
            id=str(conversation.id),
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=[
                MessageModel(
                    id=str(msg.id),
                    role=msg.role,
                    content=msg.content,
                    created_at=msg.created_at
                )
                for msg in messages
            ]
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid conversation ID")


@router.post("/conversations", response_model=ConversationModel)
async def create_conversation(
    request: ConversationCreate,
    db: AsyncSession = Depends(get_db),
    conversation_memory: ConversationMemory = Depends(get_conversation_memory)
):
    """Create a new conversation."""
    conversation = await conversation_memory.create_conversation(db, title=request.title)

    return ConversationModel(
        id=str(conversation.id),
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=[]
    )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
    conversation_memory: ConversationMemory = Depends(get_conversation_memory)
):
    """Delete a conversation."""
    try:
        conv_id = uuid.UUID(conversation_id)
        await conversation_memory.delete_conversation(db, conv_id)
        return {"message": "Conversation deleted successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid conversation ID")
