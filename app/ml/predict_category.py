import threading

import joblib

from app.services.pipeline import run_pipeline
from app.core.config import MODEL_PATH, VECTORIZER_PATH

_model = None
_vectorizer = None
_load_lock = threading.Lock()


def _load_artifacts():
    global _model, _vectorizer
    if _model is not None and _vectorizer is not None:
        return _model, _vectorizer
    with _load_lock:
        if _model is not None and _vectorizer is not None:
            return _model, _vectorizer
        try:
            model = joblib.load(MODEL_PATH)
            vectorizer = joblib.load(VECTORIZER_PATH)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Could not find model at {MODEL_PATH} or vectorizer at {VECTORIZER_PATH}"
            ) from e
        _model = model
        _vectorizer = vectorizer
        return _model, _vectorizer


def predict_category(text: str) -> dict:
    """Predict ticket category from raw text.

    Runs ``run_pipeline`` on ``text``, then infers with the trained model.
    Model and vectorizer are loaded from disk on first successful prediction
    and cached in memory for later calls.

    Args:
        text: Raw ticket text.

    Returns:
        Dict with ``category`` (str), ``score`` (float, typically 0.0–1.0), and
        ``text_processed`` (str from ``run_pipeline``).
        If preprocessing yields only whitespace, returns ``unknown`` / ``0.0`` and
        still includes ``text_processed``, without loading artifacts.

    Raises:
        FileNotFoundError: If ``MODEL_PATH`` or ``VECTORIZER_PATH`` files are missing
            when artifacts are first loaded (load is thread-safe and cached afterward).
    """
    processed_text = run_pipeline(text)

    if processed_text.strip() == "":
        return {"category": "unknown", "score": 0.0, "text_processed": processed_text}

    model, vectorizer = _load_artifacts()
    vector = vectorizer.transform([processed_text])
    categories = model.predict(vector)
    scores = model.predict_proba(vector)
    return {
        "category": str(categories[0]),
        "score": float(scores[0].max()),
        "text_processed": processed_text,
    }