"""Tests for env parsing of triage thresholds (no I/O beyond os.environ)."""

from __future__ import annotations

import pytest

from app.core.triage_settings import get_llm_min_score


def test_llm_min_score_default_when_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SMARTTICKET_LLM_MIN_SCORE", raising=False)
    assert get_llm_min_score() == 0.75


def test_llm_min_score_respects_valid_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SMARTTICKET_LLM_MIN_SCORE", "0.5")
    assert get_llm_min_score() == 0.5


def test_llm_min_score_invalid_string_falls_back(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SMARTTICKET_LLM_MIN_SCORE", "not-a-number")
    assert get_llm_min_score() == 0.75


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("1.5", 1.0),
        ("-0.1", 0.0),
        ("0", 0.0),
        ("1", 1.0),
    ],
)
def test_llm_min_score_clamped(
    monkeypatch: pytest.MonkeyPatch, raw: str, expected: float
) -> None:
    monkeypatch.setenv("SMARTTICKET_LLM_MIN_SCORE", raw)
    assert get_llm_min_score() == expected
