from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent.parent

MODEL_PATH = _REPO_ROOT / "artifacts" / "model.pkl"
VECTORIZER_PATH = _REPO_ROOT / "artifacts" / "vectorizer.pkl"
DATASET_PATH = _REPO_ROOT / "app" / "data" / "raw" / "customer_support_tickets.csv"

TEXT_COLUMN = "Ticket Description"
LABEL_COLUMN = "Ticket Type"
