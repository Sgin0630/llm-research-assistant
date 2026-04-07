from src.pdf_reader import load_pdf_for_assistant
from src.assistant import ResearchAssistant

# Test PDF reading
print("=== Loading PDF ===")
text = load_pdf_for_assistant("tests/sample.pdf")
print(f"Extracted {len(text)} characters")
print(text[:300])  # Preview first 300 chars

# Test chatting with the paper
print("\n=== Chatting with paper ===")
assistant = ResearchAssistant()
response = assistant.load_document(text, source_name="sample.pdf")
print(response)

print("\n=== Follow-up question ===")
response2 = assistant.chat("What are the main conclusions of this paper?")
print(response2)