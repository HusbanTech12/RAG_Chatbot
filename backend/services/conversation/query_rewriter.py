from typing import List, Dict
from google import genai
from google.genai import types


class QueryRewriter:
    """Rewrites queries using conversation context for better retrieval using Gemini."""

    def __init__(self, api_key: str, model: str = "models/gemini-2.5-flash"):
        """
        Initialize the query rewriter.

        Args:
            api_key: Gemini API key
            model: Gemini model to use
        """
        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def rewrite_with_context(
        self,
        query: str,
        conversation_history: List[Dict]
    ) -> str:
        """
        Rewrite query using conversation context.

        Args:
            query: Current user query
            conversation_history: Previous messages

        Returns:
            Rewritten query
        """
        # If no history or query is already detailed, return as-is
        if not conversation_history or len(query.split()) > 10:
            return query

        try:
            # Build context from recent messages
            context = self._build_context(conversation_history)

            # Create prompt for rewriting
            prompt = f"""You are a query rewriting assistant. Given a conversation history and a follow-up query, rewrite the query to be standalone and self-contained. Resolve pronouns (it, that, this, they) and add necessary context. Keep the rewritten query concise but complete. Only output the rewritten query, nothing else.

Conversation history:
{context}

Follow-up query: {query}

Rewritten query:"""

            # Get rewritten query
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=100,
                )
            )

            rewritten = response.text.strip()

            # Validate rewritten query
            if rewritten and len(rewritten) > 5:
                return rewritten
            else:
                return query

        except Exception as e:
            print(f"Error rewriting query: {e}")
            return query  # Fallback to original query

    def _build_context(self, conversation_history: List[Dict]) -> str:
        """
        Build context string from conversation history.

        Args:
            conversation_history: List of messages

        Returns:
            Context string
        """
        context_parts = []
        for msg in conversation_history[-5:]:  # Last 5 messages
            role = msg['role'].capitalize()
            content = msg['content']
            context_parts.append(f"{role}: {content}")

        return "\n".join(context_parts)
