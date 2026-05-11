from typing import List, Dict
from services.rag.vector_store import VectorStore
from services.rag.embeddings import EmbeddingService


class Retriever:
    """Retrieves relevant documents using hybrid search."""

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_service: EmbeddingService
    ):
        """
        Initialize the retriever.

        Args:
            vector_store: Vector store instance
            embedding_service: Embedding service instance
        """
        self.vector_store = vector_store
        self.embedding_service = embedding_service

    async def retrieve(
        self,
        query: str,
        n_results: int = 5,
        use_hybrid: bool = True
    ) -> List[Dict]:
        """
        Retrieve relevant documents for a query.

        Args:
            query: Search query
            n_results: Number of results to return
            use_hybrid: Whether to use hybrid search (semantic + keyword)

        Returns:
            List of relevant documents with scores
        """
        # Preprocess query
        processed_query = self._preprocess_query(query)

        # Generate query embedding
        query_embedding = await self.embedding_service.embed(processed_query)

        # Perform search
        if use_hybrid:
            results = await self.vector_store.hybrid_search(
                query=processed_query,
                query_embedding=query_embedding,
                n_results=n_results
            )
        else:
            semantic_results = await self.vector_store.semantic_search(
                query_embedding=query_embedding,
                n_results=n_results
            )

            # Format results
            results = []
            for i in range(len(semantic_results['ids'][0])):
                results.append({
                    'id': semantic_results['ids'][0][i],
                    'text': semantic_results['documents'][0][i],
                    'metadata': semantic_results['metadatas'][0][i],
                    'distance': semantic_results['distances'][0][i]
                })

        return results

    def _preprocess_query(self, query: str) -> str:
        """
        Preprocess query for better retrieval.

        Args:
            query: Raw query

        Returns:
            Preprocessed query
        """
        # Basic preprocessing: strip whitespace
        query = query.strip()

        # Could add more preprocessing here:
        # - Remove special characters
        # - Lowercase (but we keep case for now)
        # - Expand abbreviations
        # - etc.

        return query
