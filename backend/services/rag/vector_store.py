from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from rank_bm25 import BM25Okapi
import numpy as np


class VectorStore:
    """Interface to ChromaDB vector database with hybrid search support."""

    def __init__(self, persist_directory: str = "./storage/chroma_db"):
        """
        Initialize the vector store.

        Args:
            persist_directory: Directory to persist ChromaDB data
        """
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )

        # Cache for BM25 (will be rebuilt when needed)
        self._bm25_index = None
        self._bm25_docs = None
        self._bm25_ids = None

    async def add_documents(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict],
        ids: List[str]
    ):
        """
        Add documents to the vector store.

        Args:
            texts: Document texts
            embeddings: Document embeddings
            metadatas: Document metadata
            ids: Document IDs
        """
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        # Invalidate BM25 cache
        self._bm25_index = None

    async def semantic_search(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict] = None
    ) -> Dict:
        """
        Perform semantic search using vector similarity.

        Args:
            query_embedding: Query embedding vector
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

    async def keyword_search(
        self,
        query: str,
        n_results: int = 5
    ) -> List[Dict]:
        """
        Perform keyword search using BM25.

        Args:
            query: Search query
            n_results: Number of results to return

        Returns:
            List of documents with BM25 scores
        """
        # Build BM25 index if not cached
        if self._bm25_index is None:
            self._build_bm25_index()

        if self._bm25_index is None or len(self._bm25_docs) == 0:
            return []

        # Tokenize query
        query_tokens = query.lower().split()

        # Get BM25 scores
        scores = self._bm25_index.get_scores(query_tokens)

        # Get top N results
        top_indices = np.argsort(scores)[::-1][:n_results]

        results = []
        for idx in top_indices:
            if scores[idx] > 0:  # Only include results with positive scores
                results.append({
                    'id': self._bm25_ids[idx],
                    'document': self._bm25_docs[idx],
                    'score': float(scores[idx])
                })

        return results

    def _build_bm25_index(self):
        """Build BM25 index from all documents in the collection."""
        # Get all documents
        all_docs = self.collection.get()

        if not all_docs['documents']:
            return

        self._bm25_docs = all_docs['documents']
        self._bm25_ids = all_docs['ids']

        # Tokenize documents
        tokenized_docs = [doc.lower().split() for doc in self._bm25_docs]

        # Build BM25 index
        self._bm25_index = BM25Okapi(tokenized_docs)

    async def hybrid_search(
        self,
        query: str,
        query_embedding: List[float],
        n_results: int = 5,
        semantic_weight: float = 0.5
    ) -> List[Dict]:
        """
        Perform hybrid search combining semantic and keyword search using RRF.

        Args:
            query: Search query text
            query_embedding: Query embedding vector
            n_results: Number of results to return
            semantic_weight: Weight for semantic search (0-1)

        Returns:
            List of documents with combined scores
        """
        # Perform both searches
        semantic_results = await self.semantic_search(query_embedding, n_results * 2)
        keyword_results = await self.keyword_search(query, n_results * 2)

        # Reciprocal Rank Fusion (RRF)
        k = 60  # RRF constant
        rrf_scores = {}

        # Add semantic search scores
        for rank, doc_id in enumerate(semantic_results['ids'][0]):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + (1 / (k + rank + 1))

        # Add keyword search scores
        for rank, result in enumerate(keyword_results):
            doc_id = result['id']
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + (1 / (k + rank + 1))

        # Sort by RRF score
        sorted_ids = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:n_results]

        # Get full documents
        results = []
        for doc_id, score in sorted_ids:
            # Find document in semantic results
            try:
                idx = semantic_results['ids'][0].index(doc_id)
                results.append({
                    'id': doc_id,
                    'text': semantic_results['documents'][0][idx],
                    'metadata': semantic_results['metadatas'][0][idx],
                    'score': score
                })
            except ValueError:
                # Document only in keyword results
                for kw_result in keyword_results:
                    if kw_result['id'] == doc_id:
                        results.append({
                            'id': doc_id,
                            'text': kw_result['document'],
                            'metadata': {},
                            'score': score
                        })
                        break

        return results

    async def delete_documents(self, ids: List[str]):
        """
        Delete documents by IDs.

        Args:
            ids: List of document IDs to delete
        """
        self.collection.delete(ids=ids)

        # Invalidate BM25 cache
        self._bm25_index = None
