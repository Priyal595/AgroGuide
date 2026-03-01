from rag.generator import FarmerAssistant

# Load once (very important)
assistant = FarmerAssistant()

def ask_assistant(question):
    return assistant.answer(question)