from app.utils.text_cleaning import clean_text


def test_clean_text_lowercase():
    text = "HELLO WORLD"
    result = clean_text(text)
    assert result == "hello world"


def test_clean_text_removes_punctuation():
    text = "H.ELL.O W......!!!!OR::::LD"
    result = clean_text(text)
    assert result == "hello world"


def test_clean_text_normalizes_spaces():
    text = "      HELLO           WORLD               "
    result = clean_text(text)
    assert result == "hello world"


def test_clean_empty_input():
    text = ""
    result = clean_text(text)
    assert result == ""


def test_clean_text_preserves_accented_characters():
    text = "HELLÓ WORLD"
    result = clean_text(text)
    assert result == "helló world"


def test_clean_text_non_string_input():
    result = clean_text(None)
    assert result == ""
