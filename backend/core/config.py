from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str

    # Hugging Face
    hf_api_key: str

    # ChromaDB
    chroma_db_path: str = "./storage/chroma_db"

    # RAG Parameters
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_results: int = 5

    # LLM Parameters
    llm_model: str = "mistralai/Mistral-7B-Instruct-v0.2"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    temperature: float = 0.7
    max_tokens: int = 1000

    # Conversation
    max_conversation_history: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
