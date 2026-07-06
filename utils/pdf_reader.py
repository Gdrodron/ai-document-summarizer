from PyPDF2 import PdfReader


def extract_pdf(filepath):
    """
    Extract text from a PDF file.
    """
    reader = PdfReader(filepath)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()