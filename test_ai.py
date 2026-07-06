from utils.ai import summarize_document

sample_text = """
Python is a high-level programming language.

Flask is a lightweight web framework.

Google Gemini provides powerful AI models for developers.
"""

result = summarize_document(sample_text)

print("\n===== AI RESPONSE =====\n")
print(result)