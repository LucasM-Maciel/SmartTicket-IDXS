from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

import app.api.routes as routes

from app.db.models import Base, Ticket
from app.db.repository import save_ticket_prediction
from app.db.session import get_db
from app.main import app
from app.services.classifier import ClassificationResult


@pytest.fixture
def sqlite_session_factory(tmp_path):
    db_file = tmp_path / "persistence_tests.db"
    engine = create_engine(
        f"sqlite+pysqlite:///{db_file}",
        future=True,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    try:
        yield factory
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_save_ticket_prediction_persists_row(sqlite_session_factory) -> None:
    with sqlite_session_factory() as db:
        row = save_ticket_prediction(
            db,
            text_raw="Customer asks for cancellation",
            text_processed="customer asks cancellation",
            category="cancellation_request",
            score=0.91,
        )
        db.commit()
        db.refresh(row)

        persisted = db.get(Ticket, row.id)
        assert persisted is not None
        assert persisted.text_raw == "Customer asks for cancellation"
        assert persisted.category == "cancellation_request"
        assert persisted.score == 0.91


def test_post_predict_persists_ticket_with_db_dependency(
    monkeypatch: pytest.MonkeyPatch,
    sqlite_session_factory,
) -> None:
    def override_get_db() -> Generator[Session, None, None]:
        db = sqlite_session_factory()
        try:
            yield db
        finally:
            db.close()

    def fake_classify(_: str) -> ClassificationResult:
        return ClassificationResult(
            category="billing_inquiry",
            score=0.87,
            text_processed="billing issue processed",
        )

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(routes, "classify_ticket", fake_classify)

    with TestClient(app) as client:
        response = client.post("/predict", json={"text": "I was billed twice"})
    app.dependency_overrides.clear()

    assert response.status_code == 200

    with sqlite_session_factory() as db:
        rows = db.execute(select(Ticket)).scalars().all()
    assert len(rows) == 1
    assert rows[0].text_raw == "I was billed twice"
    assert rows[0].text_processed == "billing issue processed"
    assert rows[0].category == "billing_inquiry"


def test_post_predict_returns_503_and_rolls_back_when_commit_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _FailingSession:
        rolled_back = False

        def add(self, _row) -> None:
            return None

        def flush(self) -> None:
            return None

        def commit(self) -> None:
            raise SQLAlchemyError("commit failed")

        def rollback(self) -> None:
            self.rolled_back = True

    failing_session = _FailingSession()

    def override_get_db():
        return failing_session

    def fake_classify(_: str) -> ClassificationResult:
        return ClassificationResult(
            category="technical_issue",
            score=0.75,
            text_processed="technical issue processed",
        )

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(routes, "classify_ticket", fake_classify)

    with TestClient(app) as client:
        response = client.post("/predict", json={"text": "The app keeps crashing"})
    app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json()["detail"] == "Could not persist ticket; database unavailable."
    assert failing_session.rolled_back is True


def test_post_predict_returns_503_when_database_not_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_classify(_: str) -> ClassificationResult:
        return ClassificationResult(
            category="technical_issue",
            score=0.82,
            text_processed="technical issue processed",
        )

    app.dependency_overrides.clear()
    monkeypatch.setattr(routes, "classify_ticket", fake_classify)

    with TestClient(app) as client:
        response = client.post("/predict", json={"text": "My internet is unstable"})

    assert response.status_code == 503
    assert response.json()["detail"] == "Database persistence not configured."
