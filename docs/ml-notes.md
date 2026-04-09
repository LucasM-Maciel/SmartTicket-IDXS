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

## Dataset

* Current: `customer_support_tickets.csv` (8.469 rows, 5 balanced classes)
* **Issue:** dataset is synthetic — ticket descriptions have no clear semantic relationship with the labels
* Accuracy metrics from current training are not reliable indicators of real-world performance
* **Action needed:** replace with a real-world customer support dataset
* **Future:** Portuguese dataset needed to enable multilingual support

---

## Confidence Threshold

* Score ≥ 0.75 → reliable classification — LLM can attempt automatic resolution
* Score < 0.75 → goes directly to human queue with "low confidence" flag

---

## Classification Strategy — Multi-Message Conversations

In practice, the first customer message may not clearly describe the problem (e.g. "Hi, how are you?" → "I need help" → "it's about my charge").

**MVP — Approach A:**
Classify on the first message. If score < 0.75, wait for the next message, concatenate, and reclassify. Repeat until threshold is reached or N messages (configurable, default: 3).

**Future — Approach B:**
Train the model with accumulated conversation messages as a single context, separated by a delimiter. More accurate for vague openers. Requires real conversation history data collected during pilot client phase.

> Decision: Approach A for MVP, Approach B after 3 months of real pilot client data.

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
* `train_model` implemented in `app/ml/train.py` (TF-IDF + Logistic Regression, 75/25 split, artifacts saved via `joblib`)
* `predict` implemented in `app/ml/predict.py` (returns predicted category + confidence score)
* Non-string inputs handled in both preprocessing functions: returns empty string to keep pipeline safe
* First training run completed — results not representative due to synthetic dataset (see Dataset note below)

---

## Feedback Loop (Planned)

Agent corrections feed automatic model retraining:

```
Agent corrects wrong classification
→ Feedback saved (ticket_id + correct_category)
→ Accumulates N feedbacks (e.g. 500)
→ Retraining job runs automatically
→ Metrics compared with previous model
→ If better → replaces model in production
→ If worse  → keeps previous and alerts team
```

Over time the model learns the specific vocabulary of each client, generating value-based lock-in.

---

## Future Improvements

* Try Naive Bayes
* Try SVM
* Improve preprocessing
* Hyperparameter tuning
* Multilingual support: separate model per language (English and Portuguese) — pipeline already accepts `language` parameter
* Approach B: train with accumulated conversation messages for better classification on vague openers

```