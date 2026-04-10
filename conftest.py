from pathlib import Path
from typing import NamedTuple

import pytest

# conftest na raiz do repo → fixtures em tests/fixtures/
_TESTS_DIR = Path(__file__).resolve().parent / "tests"


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
    """CSV whose text column becomes empty for every row after run_pipeline (stopwords only)."""
    return _TESTS_DIR / "fixtures" / "empty_after_pipeline.csv"
