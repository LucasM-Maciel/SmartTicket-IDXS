"""Write paths for ticket persistence."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import Ticket


def save_ticket_prediction(
    db: Session,
    *,
    text_raw: str,
    text_processed: str,
    category: str,
    score: float,
    urgency: str,
    queue_target: str,
    status: str = "classified",
) -> Ticket:
    row = Ticket(
        text_raw=text_raw,
        text_processed=text_processed,
        category=category,
        score=score,
        urgency=urgency,
        queue_target=queue_target,
        status=status,
    )
    db.add(row)
    db.flush()
    return row
