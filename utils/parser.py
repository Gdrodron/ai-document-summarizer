import re

SECTION_PATTERNS = {
    "summary": re.compile(r"^#{1,3}\s*summary\s*:?\s*$", re.IGNORECASE),
    "key_points": re.compile(r"^#{1,3}\s*key points\s*:?\s*$", re.IGNORECASE),
    "action_items": re.compile(r"^#{1,3}\s*action items\s*:?\s*$", re.IGNORECASE),
    "keywords": re.compile(r"^#{1,3}\s*keywords\s*:?\s*$", re.IGNORECASE),
}


def parse_ai_response(response: str) -> dict:
    """
    Parse the AI's Markdown-formatted response into its four sections.

    Only lines that are actual Markdown headings (e.g. "## Summary") are
    treated as section boundaries. Plain body text that happens to
    contain a section name (e.g. a bullet point mentioning "summary")
    is left alone and stays inside the section it belongs to.
    """

    sections = {name: [] for name in SECTION_PATTERNS}
    current = None

    if not response:
        return {name: "" for name in SECTION_PATTERNS}

    for line in response.splitlines():
        line = line.strip()

        if not line:
            continue

        matched_section = None

        for name, pattern in SECTION_PATTERNS.items():
            if pattern.match(line):
                matched_section = name
                break

        if matched_section:
            current = matched_section
            continue

        if current:
            sections[current].append(line)

    return {
        name: "\n".join(lines).strip()
        for name, lines in sections.items()
    }