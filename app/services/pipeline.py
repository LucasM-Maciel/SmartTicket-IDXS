from app.utils.text_cleaning import clean_text
from app.utils.normalizer import normalize_text

def run_pipeline(text: str, language: str = "english") -> str:
    """Run the text preprocessing pipeline."""
    cleaned_text = clean_text(text)
    normalized_text = normalize_text(cleaned_text, language)
    return normalized_text

