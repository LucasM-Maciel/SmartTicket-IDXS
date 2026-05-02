"""Ensure NLTK resources used by the preprocessing pipeline exist at runtime.

Railway and other slim images often ship without ``nltk_data``; without stopwords,
``normalize_text`` could degrade (see ``app.utils.normalizer`` fallback). Starting
the API downloads **stopwords** once when missing so training-time and inference-time
pipelines match when possible.
"""

from __future__ import annotations

import nltk


def ensure_nltk_stopwords() -> None:
    """Download English stopwords corpus if not already present (no-op when cached)."""
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords", quiet=True)
