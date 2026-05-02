"""Unit tests for deterministic urgency + routing rules (no DB)."""

from __future__ import annotations

import pytest

from app.services.ticket_triage import (
    DEFAULT_URGENCY_FOR_UNKNOWN,
    URGENCY_HIGH,
    URGENCY_LOW,
    URGENCY_MEDIUM,
    QUEUE_HUMAN,
    QUEUE_LLM,
    normalize_predicted_category,
    routing_for_score,
    triage_prediction,
    urgency_for_category,
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("billing_inquiry", URGENCY_LOW),
        ("technical_issue", URGENCY_MEDIUM),
        ("product_inquiry", URGENCY_MEDIUM),
        ("refund_request", URGENCY_HIGH),
        ("cancellation_request", URGENCY_HIGH),
        ("Billing Inquiry", URGENCY_LOW),
        ("cancellation request", URGENCY_HIGH),
        ("unknown_label_xyz", DEFAULT_URGENCY_FOR_UNKNOWN),
    ],
)
def test_urgency_for_category(raw: str, expected: str) -> None:
    assert urgency_for_category(raw) == expected


def test_normalize_predicted_category() -> None:
    assert normalize_predicted_category("  Refund Request ") == "refund_request"


@pytest.mark.parametrize(
    ("score", "threshold", "expected"),
    [
        (0.74, 0.75, QUEUE_HUMAN),
        (0.75, 0.75, QUEUE_LLM),
        (0.99, 0.75, QUEUE_LLM),
        (0.0, 0.5, QUEUE_HUMAN),
        (0.5, 0.5, QUEUE_LLM),
    ],
)
def test_routing_for_score(score: float, threshold: float, expected: str) -> None:
    assert routing_for_score(score, llm_min_score=threshold) == expected


def test_triage_prediction_tuple() -> None:
    u, q = triage_prediction("billing_inquiry", 0.9, llm_min_score=0.75)
    assert u == URGENCY_LOW
    assert q == QUEUE_LLM
