````md id="mlnotes001"
# ML Notes

## Objective
Classify customer messages into predefined categories

---

## Categories (Initial)

- technical_issue
- billing_inquiry
- refund_request
- cancellation_request
- product_inquiry

Source: `customer_support_tickets.csv` → column `Ticket Type`

---

## Pipeline

```text
text → clean → normalize → vectorize (TF-IDF) → model
````

---

## Model

* Logistic Regression (baseline)

---

## Features

* TF-IDF vectors (primary input: `Ticket Description`)
* Future: combine `Ticket Subject` + `Ticket Description`

---

## Evaluation Metrics

* Accuracy
* Precision
* Recall
* F1-score

---

## Current Status

* Project structure created
* Pipeline defined (not fully implemented yet)
* Dataset sourced: `customer_support_tickets.csv` (8.469 rows, 5 balanced classes)
* Input column: `Ticket Description`
* Label column: `Ticket Type`
* `clean_text` implemented in `app/utils/text_cleaning.py` (lowercase, strip, regex symbol removal, whitespace normalization)
* `normalize_text` implemented in `app/utils/normalizer.py` (stopword removal via NLTK, configurable language, defaults to English)
* `run_pipeline` implemented in `app/services/pipeline.py` (orchestrates `clean_text` → `normalize_text`)
* Non-string inputs handled in both functions: returns empty string to keep pipeline safe

---

## Future Improvements

* Try Naive Bayes
* Try SVM
* Improve preprocessing
* Hyperparameter tuning

```