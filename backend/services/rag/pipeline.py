from typing import AsyncGenerator, List, Dict
from google import genai
from google.genai import types
from services.rag.retrieval import Retriever
import json
import asyncio


class RAGPipeline:
    """Complete RAG pipeline for question answering with streaming using Gemini."""

    def __init__(
        self,
        retriever: Retriever,
        api_key: str,
        model: str = "models/gemini-2.5-flash",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        """
        Initialize the RAG pipeline.

        Args:
            retriever: Retriever instance
            api_key: Gemini API key
            model: Gemini model to use
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
        """
        self.retriever = retriever
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def generate_response(
        self,
        query: str,
        conversation_history: List[Dict] = None,
        n_results: int = 5,
        max_retries: int = 3
    ) -> AsyncGenerator[Dict, None]:
        """
        Generate a response using RAG with streaming and retry logic.

        Args:
            query: User query
            conversation_history: Previous messages in conversation
            n_results: Number of documents to retrieve
            max_retries: Maximum number of retry attempts

        Yields:
            Response chunks with tokens and metadata
        """
        try:
            # Retrieve relevant documents
            documents = await self.retriever.retrieve(query, n_results)

            # Build context from retrieved documents
            context = self._build_context(documents)

            # Create prompt
            prompt = self._create_prompt(query, context, conversation_history)

            # Try to generate response with retries
            for attempt in range(max_retries):
                try:
                    # Generate response with streaming
                    response = self.client.models.generate_content_stream(
                        model=self.model,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            temperature=self.temperature,
                            max_output_tokens=self.max_tokens,
                        )
                    )

                    # Stream tokens
                    for chunk in response:
                        if chunk.text:
                            yield {
                                'token': chunk.text,
                                'done': False
                            }

                    # Send final chunk with sources
                    yield {
                        'token': '',
                        'done': True,
                        'sources': [
                            {
                                'text': doc['text'][:200] + '...',  # Preview
                                'metadata': doc.get('metadata', {}),
                                'score': doc.get('score', doc.get('distance', 0))
                            }
                            for doc in documents[:3]  # Top 3 sources
                        ]
                    }
                    return  # Success, exit retry loop

                except Exception as e:
                    error_str = str(e)

                    # Check if it's a rate limit error
                    if '429' in error_str or 'RESOURCE_EXHAUSTED' in error_str:
                        print(f"⚠️  Rate limit hit during generation. Attempt {attempt + 1}/{max_retries}")
                        if attempt < max_retries - 1:
                            wait_time = (2 ** attempt) * 2
                            print(f"   Waiting {wait_time}s before retry...")
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            yield {
                                'token': '',
                                'done': True,
                                'error': 'API quota exceeded. Please check your Gemini API quota at https://ai.dev/rate-limit or try again later.'
                            }
                            return

                    # Check if it's a temporary server error
                    elif '503' in error_str or 'UNAVAILABLE' in error_str:
                        print(f"⚠️  Server temporarily unavailable. Attempt {attempt + 1}/{max_retries}")
                        if attempt < max_retries - 1:
                            wait_time = (2 ** attempt) * 3
                            print(f"   Waiting {wait_time}s before retry...")
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            yield {
                                'token': '',
                                'done': True,
                                'error': 'Gemini API is experiencing high demand. Please try again in a few minutes.'
                            }
                            return

                    # Other errors
                    print(f"Error in RAG pipeline: {e}")
                    raise

        except Exception as e:
            error_str = str(e)
            print(f"Error in RAG pipeline: {e}")

            # Provide user-friendly error messages
            if '429' in error_str or 'RESOURCE_EXHAUSTED' in error_str:
                error_msg = 'API quota exceeded. Please check your Gemini API quota or try again later.'
            elif '503' in error_str or 'UNAVAILABLE' in error_str:
                error_msg = 'Gemini API is experiencing high demand. Please try again in a few minutes.'
            else:
                error_msg = str(e)

            yield {
                'token': '',
                'done': True,
                'error': error_msg
            }

    def _build_context(self, documents: List[Dict]) -> str:
        """
        Build context string from retrieved documents.

        Args:
            documents: Retrieved documents

        Returns:
            Context string
        """
        if not documents:
            return "No relevant documents found."

        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"[Document {i}]\n{doc['text']}\n")

        return "\n".join(context_parts)

    def _create_prompt(
        self,
        query: str,
        context: str,
        conversation_history: List[Dict] = None
    ) -> str:
        """
        Create prompt for the LLM.

        Args:
            query: User query
            context: Retrieved context
            conversation_history: Previous messages

        Returns:
            Complete prompt string
        """
        system_instruction = (
            "You are a helpful AI assistant that answers questions based on the provided context. "
            "Always ground your answers in the context provided. "
            "If the context doesn't contain enough information to answer the question, say so. "
            "Be concise and accurate."
        )

        prompt_parts = [system_instruction, "\n\n"]

        # Add conversation history if provided
        if conversation_history:
            prompt_parts.append("Conversation History:\n")
            for msg in conversation_history[-10:]:  # Last 10 messages
                role = msg['role'].capitalize()
                content = msg['content']
                prompt_parts.append(f"{role}: {content}\n")
            prompt_parts.append("\n")

        # Add context and query
        prompt_parts.append(f"Context:\n{context}\n\n")
        prompt_parts.append(f"Question: {query}\n\n")
        prompt_parts.append("Answer:")

        return "".join(prompt_parts)
