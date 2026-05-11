from typing import List, Dict, AsyncGenerator
from huggingface_hub import InferenceClient
import asyncio


class HuggingFaceRAGPipeline:
    """RAG pipeline using Hugging Face models (Free)."""

    def __init__(
        self,
        retriever,
        api_key: str,
        model: str = "mistralai/Mistral-7B-Instruct-v0.2",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        """
        Initialize the RAG pipeline.

        Args:
            retriever: Retriever instance for document retrieval
            api_key: Hugging Face API key
            model: LLM model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
        """
        self.retriever = retriever
        self.client = InferenceClient(token=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def generate_response(
        self,
        query: str,
        conversation_history: List[Dict],
        n_results: int = 5
    ) -> AsyncGenerator[Dict, None]:
        """
        Generate streaming response using RAG.

        Args:
            query: User query
            conversation_history: Previous messages
            n_results: Number of documents to retrieve

        Yields:
            Response chunks
        """
        try:
            # Retrieve relevant documents
            documents = await self.retriever.retrieve(query, n_results)

            # Build context from retrieved documents
            context = self._build_context(documents)

            # Create prompt
            prompt = self._create_prompt(query, context, conversation_history)

            # Generate response with streaming
            loop = asyncio.get_event_loop()

            # Run streaming in executor
            response_text = await loop.run_in_executor(
                None,
                lambda: self.client.text_generation(
                    prompt,
                    model=self.model,
                    max_new_tokens=self.max_tokens,
                    temperature=self.temperature,
                    return_full_text=False
                )
            )

            # Yield the response in chunks (simulate streaming)
            words = response_text.split()
            for i, word in enumerate(words):
                yield {
                    'token': word + (' ' if i < len(words) - 1 else ''),
                    'done': False
                }
                await asyncio.sleep(0.01)  # Small delay for streaming effect

            # Send final chunk with sources
            yield {
                'done': True,
                'sources': [
                    {
                        'text': doc['text'][:200] + '...',
                        'metadata': doc.get('metadata', {})
                    }
                    for doc in documents[:3]
                ]
            }

        except Exception as e:
            print(f"Error generating response: {e}")
            yield {
                'error': str(e),
                'done': True
            }

    def _build_context(self, documents: List[Dict]) -> str:
        """Build context string from retrieved documents."""
        if not documents:
            return "No relevant documents found."

        context_parts = []
        for i, doc in enumerate(documents, 1):
            text = doc.get('text', '')
            context_parts.append(f"[Document {i}]\n{text}\n")

        return "\n".join(context_parts)

    def _create_prompt(
        self,
        query: str,
        context: str,
        conversation_history: List[Dict]
    ) -> str:
        """Create prompt for the LLM."""
        # Build conversation history
        history_text = ""
        if conversation_history:
            for msg in conversation_history[-5:]:  # Last 5 messages
                role = msg['role'].capitalize()
                content = msg['content']
                history_text += f"{role}: {content}\n"

        # Create the full prompt
        prompt = f"""<s>[INST] You are a helpful AI assistant. Answer the user's question based on the provided context. If the context doesn't contain relevant information, say so.

Context:
{context}

{history_text}
User: {query}

Provide a clear, concise answer based on the context above. [/INST]"""

        return prompt
