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

## Confidence threshold (aligned with API routing)

* **ML notes / product:** Score ≥ **0.75** historically described “reliable classification” for a future LLM auto-resolve path; **below** the threshold → human review path (`queue_target: "human"` today).
* **Runtime API:** the same split is configurable via **`SMARTTICKET_LLM_MIN_SCORE`** (default **0.75**); **`routing_for_score`** uses **`>=`** (inclusive on the LLM side). Keep **`docs/ml-notes.md`**, **`docs/api-contracts.md`**, and **`.env.example`** in sync when changing the default.

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

## sklearn warnings during training smoke tests

`tests/test_train.py` (e.g. `test_train_model_valid_artifacts`) runs `train_model`, which prints scikit-learn’s `classification_report` using the small fixture at `tests/fixtures/minimal_train.csv`. With very few rows in the test split, some labels may have **no predicted samples**; sklearn then emits `UndefinedMetricWarning` (precision is ill-defined for that label). **Pytest can still report *passed* with warnings.** That is a **known side effect** of this tiny fixture plus `classification_report`—it does **not** mean the test failed, and it is **not** something you should treat as “normal” when training on the full production dataset (where metrics should be well-defined if the split and labels are sound).

To quiet the console: pass `zero_division` to `classification_report` in `app/ml/train.py`, or add a `filterwarnings` rule in pytest configuration.

---

## Current Status

* Project structure created
* Dataset sourced: `customer_support_tickets.csv` (8.469 rows, 5 balanced classes)
* Input column: `Ticket Description`
* Label column: `Ticket Type`
* `clean_text` implemented in `app/utils/text_cleaning.py` (lowercase, strip, regex symbol removal, whitespace normalization)
* `normalize_text` implemented in `app/utils/normalizer.py` (stopword removal via NLTK, configurable language, defaults to English)
* `run_pipeline` implemented in `app/services/pipeline.py` (orchestrates `clean_text` → `normalize_text`)
* `train_model` implemented in `app/ml/train.py` (TF-IDF + Logistic Regression, 75/25 split, artifacts saved via `joblib`): configurable CSV column names and output paths; rows with missing text/label are dropped; rows over `MAX_TICKET_TEXT_CHARS` are dropped; rows with empty text after `run_pipeline` are dropped before splitting
* `predict_category` implemented in `app/ml/predict_category.py` (category + confidence); blank preprocessed text → `unknown` / `0.0` without loading artifacts; lazy thread-safe load/cache of model and vectorizer from `MODEL_PATH` / `VECTORIZER_PATH`
* Column names for production CSV: `TEXT_COLUMN` / `LABEL_COLUMN` in `app/core/config.py`
* Non-string inputs handled in both preprocessing functions: returns empty string to keep pipeline safe
* First training run completed — results not representative due to synthetic dataset (see Dataset note below)
* Unit tests (pytest): `test_preprocessing.py`, `test_normalizer.py`, `test_pipeline.py`, `test_train.py`, `test_predict.py`, **`test_api.py`**, **`test_persistence.py`**, **`test_ticket_triage.py`**, **`test_triage_settings.py`** — fixtures under `tests/fixtures/`; root `conftest.py` strips **`DATABASE_URL`** during runs; see `docs/test-plan.md` and `tests/best_practices.md`
* **API + triage:** `GET /health`, `POST /predict` returns **`urgency`** + **`queue_target`**; rules in **`app/services/ticket_triage.py`**, threshold in **`app/core/triage_settings.py`**; Postgres **`db/migrations/001_add_urgency_queue_target.sql`** for existing tables; tests **`test_ticket_triage.py`**, **`test_triage_settings.py`**, updated **`test_api`** / **`test_persistence`**
* **Future (operations / feedback loop):** dedicated retrain script (e.g. `scripts/retrain.py`) when automated retraining is implemented

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

## Accent Handling Strategy

* **English (current):** accents are preserved — rare in English, no normalization needed for MVP.
* **Portuguese (future):** accent removal will be needed in `normalize_text` to handle typing variations (e.g. `"cancelamento"` vs `"cancelaménto"`). This belongs in the normalization layer, not in `clean_text`, since it is a language-specific decision.

---

## Known Preprocessing Limitations

* **Typos with punctuation between words** — e.g. `"oi,bomdia"` → `clean_text` removes the comma and produces `"oibomdia"` (unknown token). TF-IDF will assign zero weight to it, losing the tokens silently. No crash, but signal is lost.
  * Root cause: symbols are removed without inserting a space, which is the correct behavior for cases like `"H.ELL.O"` → `"HELLO"`.
  * Trade-off: fragmenting words (old behavior) was worse than merging them (current behavior).
  * Future fix: use a smarter tokenizer (e.g. `nltk.word_tokenize`) that handles punctuation context-aware.

---

## Future Improvements

* Try Naive Bayes
* Try SVM
* Improve preprocessing
* Hyperparameter tuning
* Multilingual support: separate model per language (English and Portuguese) — pipeline already accepts `language` parameter
* Approach B: train with accumulated conversation messages for better classification on vague openers
* Replace simple regex tokenization with context-aware tokenizer to handle punctuation between words

```