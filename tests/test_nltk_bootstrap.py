"""Startup NLTK bootstrap used by ``app.main`` lifespan."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from app.core.nltk_bootstrap import ensure_nltk_stopwords


def test_ensure_nltk_stopwords_downloads_when_missing() -> None:
    with patch("app.core.nltk_bootstrap.nltk") as mock_nltk:
        mock_nltk.data.find.side_effect = LookupError()
        mock_nltk.download = MagicMock()
        ensure_nltk_stopwords()
        mock_nltk.download.assert_called_once_with("stopwords", quiet=True)


def test_ensure_nltk_stopwords_skips_when_present() -> None:
    with patch("app.core.nltk_bootstrap.nltk") as mock_nltk:
        mock_nltk.data.find.return_value = "/fake/path"
        mock_nltk.download = MagicMock()
        ensure_nltk_stopwords()
        mock_nltk.download.assert_not_called()


def test_ensure_nltk_stopwords_does_not_raise_if_download_fails() -> None:
    with patch("app.core.nltk_bootstrap.nltk") as mock_nltk:
        mock_nltk.data.find.side_effect = LookupError()
        mock_nltk.download.side_effect = OSError("no network")
        ensure_nltk_stopwords()
