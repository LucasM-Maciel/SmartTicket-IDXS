from app.utils.normalizer import normalize_text


def test_normalize_text_removes_stopwords():
    text = "i want to cancel"
    result = normalize_text(text)
    assert "i" not in result.split()
    assert "to" not in result.split()
    assert "want" in result.split()
    assert "cancel" in result.split()


def test_normalize_text_empty_input():
    text = ""
    result = normalize_text(text)
    assert result == ""


def test_normalize_text_non_string_input():
    result = normalize_text(None)
    assert result == ""
