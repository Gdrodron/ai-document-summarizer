import re


def parse_ai_response(response):

    sections = {
        "summary": "",
        "key_points": "",
        "action_items": "",
        "keywords": "",
    }

    current = None

    for line in response.splitlines():

        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        if "summary" in lower:
            current = "summary"
            continue

        elif "key points" in lower:
            current = "key_points"
            continue

        elif "action items" in lower:
            current = "action_items"
            continue

        elif "keywords" in lower:
            current = "keywords"
            continue

        if current:
            sections[current] += line + "\n"

    return sections