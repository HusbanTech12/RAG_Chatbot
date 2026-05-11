from functools import lru_cache
from services.rag.embeddings import EmbeddingService
from services.rag.vector_store import VectorStore
from services.rag.chunking import DocumentChunker
from services.rag.retrieval import Retriever
from services.rag.pipeline import RAGPipeline
from services.conversation.memory import ConversationMemory
from services.conversation.query_rewriter import QueryRewriter
from core.config import get_settings

settings = get_settings()


@lru_cache()
def get_embedding_service() -> EmbeddingService:
    """Get singleton embedding service."""
    return EmbeddingService(
        api_key=settings.gemini_api_key,
        model=settings.embedding_model
    )


@lru_cache()
def get_vector_store() -> VectorStore:
    """Get singleton vector store."""
    return VectorStore(
        persist_directory=settings.chroma_db_path
    )


@lru_cache()
def get_document_chunker() -> DocumentChunker:
    """Get singleton document chunker."""
    return DocumentChunker(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap
    )


@lru_cache()
def get_retriever() -> Retriever:
    """Get singleton retriever."""
    return Retriever(
        vector_store=get_vector_store(),
        embedding_service=get_embedding_service()
    )


@lru_cache()
def get_rag_pipeline() -> RAGPipeline:
    """Get singleton RAG pipeline."""
    return RAGPipeline(
        retriever=get_retriever(),
        api_key=settings.gemini_api_key,
        model=settings.llm_model,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens
    )


@lru_cache()
def get_conversation_memory() -> ConversationMemory:
    """Get singleton conversation memory."""
    return ConversationMemory()


@lru_cache()
def get_query_rewriter() -> QueryRewriter:
    """Get singleton query rewriter."""
    return QueryRewriter(
        api_key=settings.gemini_api_key,
        model=settings.llm_model
    )
