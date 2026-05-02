import pytest

from app.ml.predict_category import predict_category
from app.ml.train import train_model


def test_predict_category_empty_string():
    text = ""
    result = predict_category(text)
    assert result["category"] == "unknown"
    assert result["score"] == 0.0
    assert "text_processed" in result


def test_predict_category_valid_format(
    minimal_train_csv,
    tmp_path,
    patch_predict_category_artifacts,
):
    model_path = tmp_path / "model.pkl"
    vectorizer_path = tmp_path / "vectorizer.pkl"
    train_model(
        minimal_train_csv,
        "text",
        "label",
        model_path=model_path,
        vectorizer_path=vectorizer_path,
    )
    patch_predict_category_artifacts(model_path, vectorizer_path)
    result = predict_category("My internet is slow today")

    assert "category" in result
    assert "score" in result
    assert isinstance(result["category"], str)
    assert isinstance(result["score"], float)
    assert 0.0 <= result["score"] <= 1.0


def test_predict_category_verify_file(tmp_path, patch_predict_category_artifacts):
    fake_model = tmp_path / "null_model.pkl"
    fake_vectorizer = tmp_path / "null_vectorizer.pkl"
    patch_predict_category_artifacts(fake_model, fake_vectorizer)

    with pytest.raises(FileNotFoundError):
        predict_category("My internet is slow today")
