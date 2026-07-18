from PyPDF2 import PdfReader


def extract_pdf(filepath):
    """
    Extract text from a PDF file.
    """
    # Open explicitly with a context manager and hand PdfReader the open
    # file object, instead of PdfReader(filepath). PdfReader(filepath)
    # opens the file internally and doesn't reliably close it right away,
    # which on Windows keeps a lock on it -- causing a PermissionError
    # later when upload.py tries to os.remove() the temp file.
    with open(filepath, "rb") as f:
        reader = PdfReader(f)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text.strip()