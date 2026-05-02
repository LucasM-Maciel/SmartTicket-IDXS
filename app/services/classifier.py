"""Facade between HTTP routes and ML inference.

Routes call ``classify_ticket`` so they depend on a stable ``ClassificationResult``
contract instead of raw dicts from ``predict_category``.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.ml.predict_category import predict_category


@dataclass(frozen=True, slots=True)
class ClassificationResult:
    """Typed output contract for ticket classification."""

    category: str
    score: float
    text_processed: str


def classify_ticket(text: str) -> ClassificationResult:
    """Run ML classification and normalize output into a typed result object."""
    raw = predict_category(text)
    return ClassificationResult(
        category=raw["category"],
        score=raw["score"],
        text_processed=raw["text_processed"],
    )
