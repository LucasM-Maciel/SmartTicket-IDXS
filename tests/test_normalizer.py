import pytest

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


def test_normalize_text_passthrough_when_stopwords_corpus_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Production hosts without ``nltk.download('stopwords')`` must still classify text."""

    def _raise(_lang: str) -> None:
        raise LookupError("no resource")

    monkeypatch.setattr(
        "app.utils.normalizer.stopwords.words",
        _raise,
    )
    assert normalize_text("my app is crashing") == "my app is crashing"
