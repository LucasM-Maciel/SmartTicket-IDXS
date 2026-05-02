from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.limits import MAX_TICKET_TEXT_CHARS
from app.services.ticket_triage import QueueTarget, UrgencyLevel


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
    urgency: UrgencyLevel
    queue_target: QueueTarget


class HealthResponse(BaseModel):
    """Minimal readiness probe — avoids exposing which artifact path is missing."""

    status: Literal["ready", "not_ready"]


class TicketQueueItem(BaseModel):
    """Single ticket row as returned by ``GET /tickets`` (ORM-backed)."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    text_raw: str
    text_processed: str
    category: str
    score: float
    urgency: UrgencyLevel
    queue_target: QueueTarget
    status: str
    created_at: datetime


class TicketQueueResponse(BaseModel):
    """Paginated queue slice plus total count for the current filter."""

    items: list[TicketQueueItem]
    total: int
    limit: int
    offset: int
