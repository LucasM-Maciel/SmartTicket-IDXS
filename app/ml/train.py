from os import PathLike
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
import pandas as pd

from app.services.pipeline import run_pipeline
from app.core.config import DATASET_PATH, MODEL_PATH, VECTORIZER_PATH, TEXT_COLUMN, LABEL_COLUMN
from app.core.limits import MAX_TICKET_TEXT_CHARS


def train_model(
    dataset: str | PathLike[str],
    texts: str,
    labels: str,
    *,
    model_path: str | PathLike[str] | None = None,
    vectorizer_path: str | PathLike[str] | None = None,
) -> None:
    """Train a TF-IDF + Logistic Regression classifier and save model and vectorizer.

    Args:
        dataset: Path to the CSV file used for training (string or path-like).
        texts: Name of the column containing ticket text.
        labels: Name of the column containing ticket labels (categories).
        model_path: Where to write the trained model; defaults to MODEL_PATH from config.
        vectorizer_path: Where to write the fitted vectorizer; defaults to VECTORIZER_PATH from config.

    Rows with missing text or label are dropped. Rows whose raw ``texts`` value
    exceeds ``MAX_TICKET_TEXT_CHARS`` (``app.core.limits``) are dropped so the
    same cap applies as on ``POST /predict``.
    """

    df = pd.read_csv(dataset)
    df = df.dropna(subset=[texts, labels])
    df = df.loc[df[texts].astype(str).str.len() <= MAX_TICKET_TEXT_CHARS]
    ticket_texts = df[texts]
    ticket_labels = df[labels]

    ticket_texts_processed = ticket_texts.apply(run_pipeline)
    mask = ticket_texts_processed != ""
    ticket_texts_processed = ticket_texts_processed[mask]
    ticket_labels = ticket_labels[mask]
    ticket_texts_train, ticket_texts_test, ticket_labels_train, ticket_labels_test = train_test_split(
        ticket_texts_processed,
        ticket_labels,
        test_size=0.25,
        random_state=42
    )

    vectorizer = TfidfVectorizer()
    ticket_texts_train_vec = vectorizer.fit_transform(ticket_texts_train)
    ticket_texts_test_vec = vectorizer.transform(ticket_texts_test)

    model = LogisticRegression(max_iter=1500)
    model.fit(ticket_texts_train_vec, ticket_labels_train)
    predictions = model.predict(ticket_texts_test_vec)
    print(
        classification_report(
            ticket_labels_test,
            predictions,
            zero_division=0,
        )
    )
    joblib.dump(model, model_path or MODEL_PATH)
    joblib.dump(vectorizer, vectorizer_path or VECTORIZER_PATH)


if __name__ == "__main__":
    train_model(DATASET_PATH, TEXT_COLUMN, LABEL_COLUMN)