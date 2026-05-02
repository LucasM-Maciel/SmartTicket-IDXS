import pytest

from app.ml.train import train_model


def test_train_model_valid_artifacts(minimal_train_csv, train_artifact_paths):
    train_model(
        minimal_train_csv,
        "text",
        "label",
        model_path=train_artifact_paths.model_path,
        vectorizer_path=train_artifact_paths.vectorizer_path,
    )
    assert train_artifact_paths.model_path.is_file()
    assert train_artifact_paths.vectorizer_path.is_file()


def test_train_model_invalid_text_name(minimal_train_csv, train_artifact_paths):
    with pytest.raises(KeyError):
        train_model(
            minimal_train_csv,
            texts="wrong_text",
            labels="label",
            model_path=train_artifact_paths.model_path,
            vectorizer_path=train_artifact_paths.vectorizer_path,
        )


def test_train_model_invalid_label_name(minimal_train_csv, train_artifact_paths):
    with pytest.raises(KeyError):
        train_model(
            minimal_train_csv,
            texts="text",
            labels="wrong_label",
            model_path=train_artifact_paths.model_path,
            vectorizer_path=train_artifact_paths.vectorizer_path,
        )


def test_train_model_empty_texts_after_pipeline(
    empty_after_pipeline_csv,
    train_artifact_paths,
):
    with pytest.raises(ValueError):
        train_model(
            empty_after_pipeline_csv,
            texts="text",
            labels="label",
            model_path=train_artifact_paths.model_path,
            vectorizer_path=train_artifact_paths.vectorizer_path,
        )
