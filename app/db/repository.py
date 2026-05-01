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
    status: str = "classified",
) -> Ticket:
    row = Ticket(
        text_raw=text_raw,
        text_processed=text_processed,
        category=category,
        score=score,
        status=status,
    )
    db.add(row)
    db.flush()
    return row
