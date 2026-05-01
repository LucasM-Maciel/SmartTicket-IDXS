from pathlib import Path
from typing import NamedTuple

import pytest


_TESTS_DIR = Path(__file__).resolve().parent / "tests"


@pytest.fixture(autouse=True)
def _isolate_database_url_for_tests(monkeypatch: pytest.MonkeyPatch) -> None:
    """Avoid hitting real Postgres when developers have ``DATABASE_URL`` in ``.env``."""
    monkeypatch.delenv("DATABASE_URL", raising=False)
    from app.db import session as db_session

    db_session.reset_db_engine_state()
    yield
    db_session.reset_db_engine_state()


class TrainArtifactPaths(NamedTuple):
    model_path: Path
    vectorizer_path: Path


@pytest.fixture
def train_artifact_paths(tmp_path) -> TrainArtifactPaths:
    return TrainArtifactPaths(
        model_path=tmp_path / "model.pkl",
        vectorizer_path=tmp_path / "vectorizer.pkl",
    )


@pytest.fixture
def minimal_train_csv():
    return _TESTS_DIR / "fixtures" / "minimal_train.csv"


@pytest.fixture
def empty_after_pipeline_csv():
    return _TESTS_DIR / "fixtures" / "empty_after_pipeline.csv"


@pytest.fixture
def patch_predict_category_artifacts(monkeypatch):
    def _patch(model_path: Path, vectorizer_path: Path) -> None:
        monkeypatch.setattr("app.ml.predict_category.MODEL_PATH", model_path)
        monkeypatch.setattr("app.ml.predict_category.VECTORIZER_PATH", vectorizer_path)
        monkeypatch.setattr("app.ml.predict_category._model", None)
        monkeypatch.setattr("app.ml.predict_category._vectorizer", None)

    return _patch
