import os

from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def summarize_document(document_text):
    """
    Generate an AI-powered summary from the extracted document.
    """

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
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error generating AI summary: {str(e)}"