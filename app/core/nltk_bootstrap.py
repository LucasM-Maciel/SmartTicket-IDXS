"""Ensure NLTK resources used by the preprocessing pipeline exist at runtime.

Railway and other slim images often ship without ``nltk_data``; without stopwords,
``normalize_text`` could degrade (see ``app.utils.normalizer`` fallback). Starting
the API downloads **stopwords** once when missing so training-time and inference-time
pipelines match when possible.

If download fails (no egress, blocked host), startup still succeeds; the normalizer
keeps a passthrough path when the corpus is absent.
"""

from __future__ import annotations

import logging

import nltk

logger = logging.getLogger(__name__)


def ensure_nltk_stopwords() -> None:
    """Download English stopwords corpus if not already present (no-op when cached)."""
    try:
        nltk.data.find("corpora/stopwords")
        return
    except LookupError:
        pass
    try:
        nltk.download("stopwords", quiet=True)
    except Exception:
        logger.warning(
            "NLTK stopwords download failed; normalize_text will passthrough if the corpus "
            "is still missing (see app.utils.normalizer).",
            exc_info=True,
        )
