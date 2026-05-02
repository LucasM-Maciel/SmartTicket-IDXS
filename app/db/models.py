"""SQLAlchemy ORM models for persistence."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, String, Text, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    text_raw: Mapped[str] = mapped_column(Text)
    text_processed: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(255))
    score: Mapped[float] = mapped_column(Float)
    urgency: Mapped[str] = mapped_column(String(32))
    queue_target: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(64), default="classified")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
