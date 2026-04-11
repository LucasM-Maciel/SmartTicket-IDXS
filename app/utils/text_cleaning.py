import re

def clean_text(text: str) -> str:
    """Normalize text to lowercase and remove symbols, emojis, and extra whitespace from raw text"""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = text.strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text