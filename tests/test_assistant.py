from src.assistant import ResearchAssistant

assistant = ResearchAssistant()

# Test basic chat
print("=== Basic chat test ===")
response = assistant.chat("What is the significance of the Schrödinger equation in quantum mechanics?")
print(response)

# Test conversation memory
print("\n=== Memory test ===")
response2 = assistant.chat("Can you give me a practical example of what you just explained?")
print(response2)