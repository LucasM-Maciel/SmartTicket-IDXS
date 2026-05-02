"""Integration tests for GET /tickets queue ordering and filters."""

from __future__ import annotations

import uuid
from collections.abc import Generator
from datetime import datetime, timezone

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.models import Ticket
from app.db.session import get_db
from app.main import app


def _ts(year: int, month: int, day: int, hour: int = 0) -> datetime:
    return datetime(year, month, day, hour, tzinfo=timezone.utc)


def _insert(
    db: Session,
    *,
    ticket_text: str,
    urgency: str,
    queue_target: str,
    created_at: datetime,
) -> None:
    db.add(
        Ticket(
            id=uuid.uuid4(),
            text_raw=ticket_text,
            text_processed=ticket_text,
            category="product_inquiry",
            score=0.8,
            urgency=urgency,
            queue_target=queue_target,
            status="classified",
            created_at=created_at,
        )
    )
    db.commit()


def test_get_tickets_orders_high_before_low_even_if_low_is_older(
    sqlite_session_factory,
) -> None:
    with sqlite_session_factory() as db:
        _insert(
            db,
            ticket_text="old low",
            urgency="LOW",
            queue_target="human",
            created_at=_ts(2026, 1, 1),
        )
        _insert(
            db,
            ticket_text="new high",
            urgency="HIGH",
            queue_target="human",
            created_at=_ts(2026, 5, 1),
        )

    def override_get_db() -> Generator[Session, None, None]:
        session = sqlite_session_factory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        response = client.get("/tickets")
    app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert [i["text_raw"] for i in body["items"]] == ["new high", "old low"]


def test_get_tickets_fifo_within_same_urgency(sqlite_session_factory) -> None:
    with sqlite_session_factory() as db:
        _insert(
            db,
            ticket_text="first",
            urgency="MEDIUM",
            queue_target="llm",
            created_at=_ts(2026, 2, 1, 10),
        )
        _insert(
            db,
            ticket_text="second",
            urgency="MEDIUM",
            queue_target="llm",
            created_at=_ts(2026, 2, 1, 11),
        )

    def override_get_db() -> Generator[Session, None, None]:
        session = sqlite_session_factory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        response = client.get("/tickets")
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert [i["text_raw"] for i in response.json()["items"]] == ["first", "second"]


def test_get_tickets_filter_by_queue_target(sqlite_session_factory) -> None:
    with sqlite_session_factory() as db:
        _insert(
            db,
            ticket_text="human only",
            urgency="HIGH",
            queue_target="human",
            created_at=_ts(2026, 3, 1),
        )
        _insert(
            db,
            ticket_text="llm only",
            urgency="HIGH",
            queue_target="llm",
            created_at=_ts(2026, 3, 2),
        )

    def override_get_db() -> Generator[Session, None, None]:
        session = sqlite_session_factory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        response = client.get("/tickets", params={"queue_target": "llm"})
    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["text_raw"] == "llm only"
    assert data["items"][0]["queue_target"] == "llm"


def test_get_tickets_pagination_total(sqlite_session_factory) -> None:
    with sqlite_session_factory() as db:
        for i in range(3):
            _insert(
                db,
                ticket_text=f"t{i}",
                urgency="LOW",
                queue_target="human",
                created_at=_ts(2026, 4, i + 1),
            )

    def override_get_db() -> Generator[Session, None, None]:
        session = sqlite_session_factory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        page0 = client.get("/tickets", params={"limit": 2, "offset": 0})
        page1 = client.get("/tickets", params={"limit": 2, "offset": 2})
    app.dependency_overrides.clear()

    assert page0.json()["total"] == 3
    assert len(page0.json()["items"]) == 2
    assert len(page1.json()["items"]) == 1


def test_get_tickets_503_when_database_not_configured() -> None:
    app.dependency_overrides.clear()
    with TestClient(app) as client:
        response = client.get("/tickets")
    assert response.status_code == 503
    assert response.json()["detail"] == "Database persistence not configured."


def test_get_tickets_rejects_invalid_queue_target() -> None:
    app.dependency_overrides.clear()
    with TestClient(app) as client:
        response = client.get("/tickets", params={"queue_target": "robot"})
    assert response.status_code == 422
