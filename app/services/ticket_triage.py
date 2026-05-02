"""Deterministic triage rules: urgency from predicted category, routing from score.

All string constants are English — aligned with the technical MVP conventions.
See ``docs/project-context.md`` (*Technical MVP closure — implementation status*).
"""

from __future__ import annotations

from typing import Literal

# Stored in DB and APIs — keep stable for queries and dashboards.
UrgencyLevel = Literal["HIGH", "MEDIUM", "LOW"]
QueueTarget = Literal["human", "llm"]

URGENCY_HIGH: UrgencyLevel = "HIGH"
URGENCY_MEDIUM: UrgencyLevel = "MEDIUM"
URGENCY_LOW: UrgencyLevel = "LOW"

QUEUE_HUMAN: QueueTarget = "human"
QUEUE_LLM: QueueTarget = "llm"

# Fallback when the classifier returns an unexpected label or ``unknown``.
DEFAULT_URGENCY_FOR_UNKNOWN: UrgencyLevel = URGENCY_MEDIUM

# Canonical predicted-category strings (must match training labels / docs).
_CATEGORY_TO_URGENCY: dict[str, UrgencyLevel] = {
    "technical_issue": URGENCY_MEDIUM,
    "product_inquiry": URGENCY_MEDIUM,
    "billing_inquiry": URGENCY_LOW,
    "refund_request": URGENCY_HIGH,
    "cancellation_request": URGENCY_HIGH,
}


def normalize_predicted_category(category: str) -> str:
    """Normalize model output for lookup (spacing/case).

    Training labels should already match the dict keys; this keeps MVP tolerant.
    """
    return category.strip().lower().replace(" ", "_").replace("-", "_")


def urgency_for_category(category: str) -> UrgencyLevel:
    """Map predicted category to urgency tier (tiered queue ordering)."""
    key = normalize_predicted_category(category)
    return _CATEGORY_TO_URGENCY.get(key, DEFAULT_URGENCY_FOR_UNKNOWN)


def routing_for_score(score: float, *, llm_min_score: float) -> QueueTarget:
    """Route by confidence: high score → LLM path, low score → human review path.

    ``score`` is inclusive on the LLM side: ``score >= llm_min_score`` → LLM.
    """
    if score >= llm_min_score:
        return QUEUE_LLM
    return QUEUE_HUMAN


def triage_prediction(category: str, score: float, *, llm_min_score: float) -> tuple[UrgencyLevel, QueueTarget]:
    """Compute persisted urgency + queue target from classification output."""
    return (
        urgency_for_category(category),
        routing_for_score(score, llm_min_score=llm_min_score),
    )
