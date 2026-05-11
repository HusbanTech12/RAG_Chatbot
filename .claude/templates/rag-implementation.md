# RAG Implementation Template

Use this template when implementing RAG functionality.

## Document Ingestion

```python
# backend/rag/ingestion.py
from typing import List
import hashlib

class DocumentChunker:
    """Splits documents into chunks for embedding."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str, metadata: dict = None) -> List[dict]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            metadata: Optional metadata to attach to each chunk
            
        Returns:
            List of chunks with metadata
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            
            chunk = {
                'text': chunk_text,
                'chunk_id': hashlib.md5(chunk_text.encode()).hexdigest(),
                'start_index': start,
                'end_index': end,
                'metadata': metadata or {}
            }
            chunks.append(chunk)
            
            start += self.chunk_size - self.chunk_overlap
        
        return chunks

class DocumentProcessor:
    """Processes and stores documents in vector database."""
    
    def __init__(self, vector_store, embedding_model):
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.chunker = DocumentChunker()
    
    async def process_document(self, document: str, metadata: dict = None):
        """
        Process a document: chunk, embed, and store.
        
        Args:
            document: Document text
            metadata: Document metadata
        """
        # Chunk the document
        chunks = self.chunker.chunk_text(document, metadata)
        
        # Generate embeddings
        texts = [chunk['text'] for chunk in chunks]
        embeddings = await self.embedding_model.embed_batch(texts)
        
        # Store in vector database
        await self.vector_store.add(
            texts=texts,
            embeddings=embeddings,
            metadatas=[chunk['metadata'] for chunk in chunks],
            ids=[chunk['chunk_id'] for chunk in chunks]
        )
```

## Embedding Generation

```python
# backend/rag/embeddings.py
from typing import List
import openai

class EmbeddingModel:
    """Generates embeddings for text."""
    
    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
        self.client = openai.AsyncOpenAI()
    
    async def embed(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        response = await self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        response = await self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]
```

## Vector Store

```python
# backend/rag/vector_store.py
from typing import List, Optional
import chromadb
from chromadb.config import Settings

class VectorStore:
    """Interface to vector database."""
    
    def __init__(self, collection_name: str = "documents"):
        self.client = chromadb.PersistentClient(
            path="./chroma_db",
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    async def add(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[dict],
        ids: List[str]
    ):
        """Add documents to the vector store."""
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
    
    async def search(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[dict] = None
    ) -> dict:
        """
        Search for similar documents.
        
        Args:
            query_embedding: Query vector
            n_results: Number of results to return
            where: Optional metadata filter
            
        Returns:
            Search results with documents and distances
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )
        return results
```

## Retrieval

```python
# backend/rag/retrieval.py
from typing import List

class Retriever:
    """Retrieves relevant documents for a query."""
    
    def __init__(self, vector_store, embedding_model):
        self.vector_store = vector_store
        self.embedding_model = embedding_model
    
    async def retrieve(
        self,
        query: str,
        n_results: int = 5,
        filters: dict = None
    ) -> List[dict]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Search query
            n_results: Number of results to return
            filters: Optional metadata filters
            
        Returns:
            List of relevant documents with scores
        """
        # Generate query embedding
        query_embedding = await self.embedding_model.embed(query)
        
        # Search vector store
        results = await self.vector_store.search(
            query_embedding=query_embedding,
            n_results=n_results,
            where=filters
        )
        
        # Format results
        documents = []
        for i, doc in enumerate(results['documents'][0]):
            documents.append({
                'text': doc,
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i],
                'id': results['ids'][0][i]
            })
        
        return documents
```

## RAG Pipeline

```python
# backend/rag/pipeline.py
from typing import AsyncGenerator
import openai

class RAGPipeline:
    """Complete RAG pipeline for question answering."""
    
    def __init__(self, retriever, llm_model: str = "gpt-4"):
        self.retriever = retriever
        self.llm_model = llm_model
        self.client = openai.AsyncOpenAI()
    
    async def generate_response(
        self,
        query: str,
        n_results: int = 5
    ) -> AsyncGenerator[str, None]:
        """
        Generate a response using RAG.
        
        Args:
            query: User query
            n_results: Number of documents to retrieve
            
        Yields:
            Response tokens as they are generated
        """
        # Retrieve relevant documents
        documents = await self.retriever.retrieve(query, n_results)
        
        # Build context from retrieved documents
        context = "\n\n".join([doc['text'] for doc in documents])
        
        # Create prompt
        prompt = f"""Answer the question based on the following context:

Context:
{context}

Question: {query}

Answer:"""
        
        # Generate response with streaming
        stream = await self.client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
```

## FastAPI Endpoint

```python
# backend/routers/chat.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1", tags=["chat"])

class ChatRequest(BaseModel):
    query: str
    n_results: int = 5

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint with RAG.
    
    Streams the response as it's generated.
    """
    async def generate():
        async for token in rag_pipeline.generate_response(
            query=request.query,
            n_results=request.n_results
        ):
            yield token
    
    return StreamingResponse(generate(), media_type="text/plain")
```
