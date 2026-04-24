from typing import Literal

from pydantic import BaseModel, Field

from app.core.limits import MAX_TICKET_TEXT_CHARS


class PredictRequest(BaseModel):
    text: str = Field(
        ...,
        max_length=MAX_TICKET_TEXT_CHARS,
        description="Raw ticket text; length capped for API hardening (see app.core.limits).",
    )


class PredictResponse(BaseModel):
    text: str
    category: str
    score: float


class HealthResponse(BaseModel):
    """Minimal readiness probe — avoids exposing which artifact path is missing."""

    status: Literal["ready", "not_ready"]
