import logging

from nltk.corpus import stopwords

logger = logging.getLogger(__name__)


def normalize_text(text: str, language: str = "english") -> str:
    """Remove stopwords from text using the specified language corpus."""
    if not isinstance(text, str):
        return ""
    try:
        stop_words = set(stopwords.words(language))
    except LookupError as e:
        logger.error(
            "NLTK stopwords unavailable for language %r: %s. "
            "Install with: nltk.download('stopwords')",
            language,
            e,
        )
        return ""
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return " ".join(filtered_words)
