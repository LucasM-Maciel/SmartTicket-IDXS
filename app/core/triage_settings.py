"""Environment-backed settings for ticket triage (urgency + LLM vs human routing).

Kept small so pure triage logic stays easy to test without importing the whole app.
"""

from __future__ import annotations

import os

_DEFAULT_LLM_MIN_SCORE = 0.75


def _clamp_unit_interval(value: float) -> float:
    """Keep threshold in [0.0, 1.0] so routing stays consistent with model scores."""
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value


def get_llm_min_score() -> float:
    """Minimum classification score to route a ticket to the LLM path (inclusive).

    Reads ``SMARTTICKET_LLM_MIN_SCORE``. Missing or blank env → ``0.75``.
    Unparseable values fall back to ``0.75`` (invalid deploy config should not break every request).
    Numeric values are clamped to **[0.0, 1.0]**.
    """
    raw = os.getenv("SMARTTICKET_LLM_MIN_SCORE")
    if raw is None or not raw.strip():
        return _DEFAULT_LLM_MIN_SCORE
    try:
        parsed = float(raw.strip())
    except ValueError:
        return _DEFAULT_LLM_MIN_SCORE
    return _clamp_unit_interval(parsed)
