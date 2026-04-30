# test_gemini.py  (root mein)

from app.infrastructure.llm.gemini_client import gemini_client

response = gemini_client.generate("Say hello in one line only.")
print("Gemini:", response)