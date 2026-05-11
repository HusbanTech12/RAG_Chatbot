from typing import List
from google import genai
from google.genai import types
import tiktoken
import time
import asyncio


class EmbeddingService:
    """Service for generating embeddings using Google Gemini."""

    def __init__(self, api_key: str, model: str = "models/gemini-embedding-2"):
        """
        Initialize the embedding service.

        Args:
            api_key: Gemini API key
            model: Embedding model to use
        """
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.encoding = tiktoken.get_encoding("cl100k_base")

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
                result = self.client.models.embed_content(
                    model=self.model,
                    contents=text,
                    config=types.EmbedContentConfig(
                        task_type="RETRIEVAL_DOCUMENT"
                    )
                )
                return result.embeddings[0].values
            except Exception as e:
                error_str = str(e)

                # Check if it's a rate limit or quota error
                if '429' in error_str or 'RESOURCE_EXHAUSTED' in error_str:
                    print(f"⚠️  Rate limit hit. Attempt {attempt + 1}/{max_retries}")
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) * 2  # Exponential backoff: 2s, 4s, 8s
                        print(f"   Waiting {wait_time}s before retry...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        print(f"❌ Rate limit exceeded after {max_retries} attempts")
                        raise Exception("API quota exceeded. Please check your Gemini API quota at https://ai.dev/rate-limit")

                # Check if it's a temporary server error
                elif '503' in error_str or 'UNAVAILABLE' in error_str:
                    print(f"⚠️  Server temporarily unavailable. Attempt {attempt + 1}/{max_retries}")
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) * 3  # Exponential backoff: 3s, 6s, 12s
                        print(f"   Waiting {wait_time}s before retry...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        print(f"❌ Server unavailable after {max_retries} attempts")
                        raise Exception("Gemini API is temporarily unavailable. Please try again in a few minutes.")

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
                    await asyncio.sleep(0.5)

            except Exception as e:
                print(f"Error embedding chunk {i + 1}: {e}")
                raise

        return embeddings

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text.

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens
        """
        return len(self.encoding.encode(text))
