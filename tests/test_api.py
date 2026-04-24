import pytest
from fastapi.testclient import TestClient

from app.core.limits import MAX_TICKET_TEXT_CHARS
from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_get_health_response_shape(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code in (200, 503)
    data = response.json()
    assert data["status"] in ("ready", "not_ready")
    assert set(data.keys()) == {"status"}


def test_post_predict_success(monkeypatch: pytest.MonkeyPatch, client: TestClient) -> None:
    import app.api.routes as routes

    def fake_predict(text: str) -> dict:
        return {"category": "test_category", "score": 0.99}

    monkeypatch.setattr(routes, "predict_category", fake_predict)
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
    import app.api.routes as routes

    def raise_missing(_: str) -> dict:
        raise FileNotFoundError()

    monkeypatch.setattr(routes, "predict_category", raise_missing)
    response = client.post("/predict", json={"text": "valid body"})
    assert response.status_code == 503
    assert response.json()["detail"] == "Model artifacts missing; check GET /health"
