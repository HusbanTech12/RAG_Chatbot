from typing import List
from huggingface_hub import InferenceClient
import asyncio


class HuggingFaceEmbeddingService:
    """Service for generating embeddings using Hugging Face (Free)."""

    def __init__(self, api_key: str, model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedding service.

        Args:
            api_key: Hugging Face API key (free from https://huggingface.co/settings/tokens)
            model: Embedding model to use
        """
        self.client = InferenceClient(token=api_key)
        self.model = model

    async def embed(self, text: str, max_retries: int = 3) -> List[float]:
        """
        Generate embedding for a single text with retry logic.

        Args:
            text: Text to embed
            max_retries: Maximum number of retry attempts

        Returns:
            Embedding vector
        """
        for attempt in range(max_retries):
            try:
                # Run in thread pool since HF client is synchronous
                loop = asyncio.get_event_loop()
                embedding = await loop.run_in_executor(
                    None,
                    lambda: self.client.feature_extraction(text, model=self.model)
                )

                # Convert to list if needed
                if hasattr(embedding, 'tolist'):
                    embedding = embedding.tolist()

                return embedding

            except Exception as e:
                error_str = str(e)

                # Check if it's a rate limit error
                if '429' in error_str or 'rate limit' in error_str.lower():
                    print(f"⚠️  Rate limit hit. Attempt {attempt + 1}/{max_retries}")
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) * 2  # Exponential backoff
                        print(f"   Waiting {wait_time}s before retry...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        print(f"❌ Rate limit exceeded after {max_retries} attempts")
                        raise Exception("Hugging Face API rate limit exceeded. Please wait a moment and try again.")

                # Check if it's a temporary server error
                elif '503' in error_str or 'unavailable' in error_str.lower():
                    print(f"⚠️  Server temporarily unavailable. Attempt {attempt + 1}/{max_retries}")
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) * 3
                        print(f"   Waiting {wait_time}s before retry...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        print(f"❌ Server unavailable after {max_retries} attempts")
                        raise Exception("Hugging Face API is temporarily unavailable. Please try again in a few minutes.")

                # Other errors
                print(f"Error generating embedding: {e}")
                raise

    async def embed_batch(self, texts: List[str], max_retries: int = 3) -> List[List[float]]:
        """
        Generate embeddings for multiple texts with retry logic.

        Args:
            texts: List of texts to embed
            max_retries: Maximum number of retry attempts

        Returns:
            List of embedding vectors
        """
        embeddings = []

        # Process one at a time to avoid hitting rate limits
        for i, text in enumerate(texts):
            print(f"Embedding chunk {i + 1}/{len(texts)}...")
            try:
                embedding = await self.embed(text, max_retries=max_retries)
                embeddings.append(embedding)

                # Add small delay between requests to avoid rate limits
                if i < len(texts) - 1:
                    await asyncio.sleep(1)  # HF free tier has stricter limits

            except Exception as e:
                print(f"Error embedding chunk {i + 1}: {e}")
                raise

        return embeddings
