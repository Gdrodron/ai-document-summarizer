from utils.pdf_reader import extract_pdf
from utils.docx_reader import extract_docx
from utils.txt_reader import extract_txt


def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """Return True if filename has an extension present in allowed_extensions."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in allowed_extensions
    )


def extract_text(filepath: str, extension: str) -> str:
    """
    Extract text from a file based on its extension.

    Raises:
        ValueError: if the extension is not supported.
    """

    extension = extension.lower().lstrip(".")

    if extension == "pdf":
        return extract_pdf(filepath)

    if extension == "docx":
        return extract_docx(filepath)

    if extension == "txt":
        return extract_txt(filepath)

    raise ValueError(f"Unsupported file type: .{extension}")