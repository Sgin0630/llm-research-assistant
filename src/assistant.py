import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class ResearchAssistant:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.conversation_history = []
        self.system_prompt = """You are an expert research assistant with a background in 
science and academia. When given research papers or documents, you help users understand 
them deeply — summarizing key findings, explaining technical concepts clearly, identifying 
methodology, and answering follow-up questions.

When no document is provided, you answer research questions using your own knowledge.
Always be precise, cite specific parts of the provided text when relevant, and flag 
any limitations or uncertainties in the research."""

    def chat(self, user_message: str) -> str:
        """Send a message and get a response, maintaining conversation history."""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=self.system_prompt,
            messages=self.conversation_history
        )

        assistant_message = response.content[0].text

        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def load_document(self, document_text: str, source_name: str = "document"):
        """Inject a document into the conversation as context."""
        context_message = f"""I've loaded the following document for our conversation: '{source_name}'

--- DOCUMENT START ---
{document_text}
--- DOCUMENT END ---

Please confirm you've read it and give a brief 2-3 sentence overview of what it covers."""
        
        return self.chat(context_message)

    def clear_history(self):
        """Reset the conversation."""
        self.conversation_history = []