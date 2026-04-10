import os
from anthropic import Anthropic
from dotenv import load_dotenv

from src.generation.prompts import PHYSICS_SYSTEM_PROMPT
from src.generation.citations import format_citations

load_dotenv()


class HEPAssistant:
    """Physics-domain RAG assistant backed by Claude and hybrid retrieval."""

    def __init__(self, retriever=None):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.retriever = retriever
        self.conversation_history = []

    def chat(self, query: str, top_k: int = 5) -> tuple[str, list[dict]]:
        """
        Retrieve relevant chunks, build context, call Claude, format citations.
        Returns (response_text, source_docs).
        """
        source_docs = []
        context = ""

        if self.retriever is not None:
            source_docs = self.retriever.retrieve(query, top_k=top_k)
            if source_docs:
                context_parts = []
                for doc in source_docs:
                    arxiv_id = doc.get("arxiv_id", "unknown")
                    context_parts.append(
                        f"[arXiv:{arxiv_id}]\n{doc['text']}"
                    )
                context = "--- RETRIEVED CONTEXT ---\n\n" + "\n\n---\n\n".join(context_parts) + "\n\n---"

        user_content = f"{context}\n\n{query}" if context else query

        self.conversation_history.append({"role": "user", "content": user_content})

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=PHYSICS_SYSTEM_PROMPT,
            messages=self.conversation_history,
        )

        assistant_message = response.content[0].text
        assistant_message = format_citations(assistant_message, source_docs)

        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        return assistant_message, source_docs

    def clear_history(self) -> None:
        """Reset conversation history."""
        self.conversation_history = []
