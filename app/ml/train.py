from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
import pandas as pd

from app.services.pipeline import run_pipeline
from app.core.config import DATASET_PATH, MODEL_PATH, VECTORIZER_PATH


def train_model(dataset: str):
    """Load dataset, train a TF-IDF + Logistic Regression model, and save artifacts to disk."""
    df = pd.read_csv(dataset)
    ticket_texts = df["Ticket Description"]
    ticket_labels = df["Ticket Type"]

    ticket_texts_processed = ticket_texts.apply(run_pipeline)
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
    print(classification_report(ticket_labels_test, predictions))
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

if __name__ == "__main__":
    train_model(DATASET_PATH)