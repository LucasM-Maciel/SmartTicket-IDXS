import joblib
import sys

from app.services.pipeline import run_pipeline
from app.core.config import MODEL_PATH, VECTORIZER_PATH


try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
except FileNotFoundError:
    sys.exit(f"Artifacts not found. Run train.py first. Expected: {MODEL_PATH}")


def predict(text: str) -> dict:
    """Load trained model and vectorizer, and predict the category of a given text."""
    processed_text = run_pipeline(text)
    
    if processed_text.strip() == "":
        return {"category": "unknown", "score": 0.0}
           

    vector = vectorizer.transform([processed_text])
    categories = model.predict(vector)
    scores = model.predict_proba(vector)
    return {"category": categories[0], "score": float(scores[0].max())}