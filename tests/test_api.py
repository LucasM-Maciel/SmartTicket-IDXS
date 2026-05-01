import pytest
from fastapi.testclient import TestClient

import app.api.routes as routes
from app.core.limits import MAX_TICKET_TEXT_CHARS
from app.db.session import get_db
from app.main import app
from app.services.classifier import ClassificationResult


@pytest.fixture
def client() -> TestClient:
    class _DummySession:
        def add(self, _row) -> None:
            return None

        def flush(self) -> None:
            return None

        def commit(self) -> None:
            return None

        def rollback(self) -> None:
            return None

    def _override_get_db():
        return _DummySession()

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_get_health_response_shape(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code in (200, 503)
    data = response.json()
    assert data["status"] in ("ready", "not_ready")
    assert set(data.keys()) == {"status"}


def test_post_predict_success(monkeypatch: pytest.MonkeyPatch, client: TestClient) -> None:
    def fake_classify(text: str) -> ClassificationResult:
        return ClassificationResult(
            category="test_category",
            score=0.99,
            text_processed=text.lower(),
        )

    monkeypatch.setattr(routes, "classify_ticket", fake_classify)
    response = client.post("/predict", json={"text": "I need help with my internet"})
    assert response.status_code == 200
    body = response.json()
    assert body["text"] == "I need help with my internet"
    assert body["category"] == "test_category"
    assert body["score"] == 0.99


def test_post_predict_validation_error(client: TestClient) -> None:
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_post_predict_rejects_text_over_max_length(client: TestClient) -> None:
    response = client.post(
        "/predict",
        json={"text": "x" * (MAX_TICKET_TEXT_CHARS + 1)},
    )
    assert response.status_code == 422


def test_post_predict_503_when_artifacts_missing(
    monkeypatch: pytest.MonkeyPatch, client: TestClient
) -> None:
    def raise_missing(_: str) -> ClassificationResult:
        raise FileNotFoundError()

    monkeypatch.setattr(routes, "classify_ticket", raise_missing)
    response = client.post("/predict", json={"text": "valid body"})
    assert response.status_code == 503
    assert response.json()["detail"] == "Model artifacts missing; check GET /health"
