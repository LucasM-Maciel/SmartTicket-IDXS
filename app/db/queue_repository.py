"""Read-only queries for the operational ticket queue (ordering + pagination).

Ordering matches product rules: tier by ``urgency`` (HIGH → MEDIUM → LOW), then
FIFO within a tier by ``created_at`` ascending.
"""

from __future__ import annotations

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.db.models import Ticket
from app.services.ticket_triage import URGENCY_HIGH, URGENCY_LOW, URGENCY_MEDIUM

# Prevent accidental huge responses (API layer also caps query params).
_MAX_LIMIT = 100
_DEFAULT_LIMIT = 50


def _urgency_rank_expression():
    """Stable SQL ordering: HIGH=0, MEDIUM=1, LOW=2, anything else last."""
    return case(
        (Ticket.urgency == URGENCY_HIGH, 0),
        (Ticket.urgency == URGENCY_MEDIUM, 1),
        (Ticket.urgency == URGENCY_LOW, 2),
        else_=3,
    )


def list_tickets_queue(
    db: Session,
    *,
    queue_target: str | None = None,
    limit: int = _DEFAULT_LIMIT,
    offset: int = 0,
) -> tuple[list[Ticket], int]:
    """Return tickets ordered for servicing and total matching the optional filter.

    ``limit`` is clamped to ``[1, _MAX_LIMIT]``; ``offset`` is clamped to ``>= 0``.
    """
    limit = min(max(int(limit), 1), _MAX_LIMIT)
    offset = max(int(offset), 0)

    stmt = select(Ticket).order_by(
        _urgency_rank_expression().asc(),
        Ticket.created_at.asc(),
    )
    count_stmt = select(func.count()).select_from(Ticket)

    if queue_target is not None:
        stmt = stmt.where(Ticket.queue_target == queue_target)
        count_stmt = count_stmt.where(Ticket.queue_target == queue_target)

    stmt = stmt.limit(limit).offset(offset)

    total = db.execute(count_stmt).scalar_one()
    rows = db.scalars(stmt).all()
    return list(rows), int(total)
