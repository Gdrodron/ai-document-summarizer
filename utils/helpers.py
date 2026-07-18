def document_statistics(text: str) -> dict:
    """Compute word count, character count, and estimated reading time."""

    text = text or ""
    word_count = len(text.split())

    return {
        "word_count": word_count,
        "character_count": len(text),
        "reading_time": max(1, round(word_count / 200)),
    }


def parse_keywords(text: str) -> list:
    """
    Split a comma-separated keyword string into a clean list.
    Strips whitespace, drops empty entries, and removes duplicates
    while preserving the original order.
    """

    if not text:
        return []

    seen = set()
    keywords = []

    for keyword in text.split(","):
        keyword = keyword.strip()

        if keyword and keyword.lower() not in seen:
            seen.add(keyword.lower())
            keywords.append(keyword)

    return keywords