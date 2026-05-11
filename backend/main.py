from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routers import chat_simple, documents_simple, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown."""
    # Startup
    print("Starting up...")
    print("Startup complete - running without database")

    yield

    # Shutdown
    print("Shutting down...")


app = FastAPI(
    title="RAG Chatbot API (Hugging Face - Free)",
    description="RAG System with Free Hugging Face Models",
    version="1.0.0-hf",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (simplified versions without database)
app.include_router(health.router)
app.include_router(chat_simple.router)
app.include_router(documents_simple.router)


@app.get("/")
def read_root():
    return {
        "message": "RAG Chatbot API",
        "version": "1.0.0",
        "docs": "/docs"
    }