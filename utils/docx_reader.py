from docx import Document


def extract_docx(filepath):
    """
    Extract text from a DOCX file.
    """
    document = Document(filepath)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text.strip()