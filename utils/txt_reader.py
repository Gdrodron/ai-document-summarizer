def extract_txt(filepath):
    """
    Extract text from a TXT file.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()