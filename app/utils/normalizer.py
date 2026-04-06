from nltk.corpus import stopwords

def normalize_text(text: str, language: str = "english") -> str:
    """Remove stopwords from text using the specified language corpus."""
    if not isinstance(text, str):
        return ""
    try:
        stop_words = set(stopwords.words(language))
    except LookupError as e:
        print(f"Error: {e}")
        print("Please download the stopwords corpus using: nltk.download('stopwords')")
        return ""
    list_of_words = text.split()
    list_of_normalized_words = [word for word in list_of_words if word not in stop_words]
    text = " ".join(list_of_normalized_words)
    return text
