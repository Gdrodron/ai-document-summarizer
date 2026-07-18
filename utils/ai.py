import os

from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Add it to your .env file before "
        "starting the app."
    )

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def summarize_document(document_text):
    """
    Generate an AI-powered summary from the extracted document.

    Raises:
        ValueError: if document_text is empty.
        RuntimeError: if the Gemini API call fails or returns no content.
    """

    if not document_text or not document_text.strip():
        raise ValueError("No text was extracted from the document.")

    prompt = f"""
You are an expert AI document analyst.

Analyze the document below.

Return your response EXACTLY in the following Markdown format.

## Summary
Provide a concise summary of the document.

## Key Points
- Bullet point
- Bullet point
- Bullet point

## Action Items
- Bullet point
- Bullet point

## Keywords
keyword1, keyword2, keyword3, keyword4

Document:

{document_text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

    except Exception as error:
        raise RuntimeError(f"Gemini API request failed: {error}") from error

    if not response.text or not response.text.strip():
        raise RuntimeError(
            "Gemini returned an empty response (it may have been "
            "blocked by a safety filter)."
        )

    return response.text