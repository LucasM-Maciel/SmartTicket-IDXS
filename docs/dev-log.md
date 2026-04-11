
<!--
🇧🇷 COMO ATUALIZAR:
- Atualize TODO DIA que trabalhar
- Seja simples: o que fez, problema, solução
- Isso mostra evolução real
-->

# Development Log

## 2026-03-31 (Lucas)

### What was done
- Project structure created
- Documentation structure created
- Defined MVP scope
- Defined pipeline architecture

### Problems
- Understanding architecture layers
- Organizing responsibilities

### Solutions
- Defined layered architecture
- Created documentation for context

### Learnings
- Pipeline must be validated before API
- Separation of concerns is critical

### Next Steps
- Implement clean_text
- Implement normalize_text
- Build first pipeline version

---

## 2026-04-06 (Lucas)

### What was done
- Created skeleton of `app/utils/text_cleaning.py`
- Implemented `clean_text` function: lowercase, strip, remove symbols via regex, normalize whitespace
- Implemented `normalize_text` in `app/utils/normalizer.py`: removes stopwords via NLTK with configurable language parameter

### Problems
- `clean_text`: function would fail if input was not a string (e.g. NaN, None from the dataset)
- `normalize_text`: challenge was keeping the code clean and readable while handling edge cases properly

### Solutions
- Non-string inputs return empty string in both functions — safe for the pipeline and avoids constant exceptions
- `LookupError` caught on NLTK corpus load: prints download instructions and returns empty string gracefully

### Learnings
- Regex is more powerful than expected — learned new patterns during implementation
- Learned more about string manipulation in Python
- Defensive input handling is better than error propagation in pipeline contexts

### Next Steps
- Implement `pipeline.py` connecting `clean_text` → `normalize_text` → vectorizer → model

---

## 2026-04-07 (Lucas)

### What was done
- Implemented `app/services/pipeline.py`: `run_pipeline` connects `clean_text` → `normalize_text`
- Implemented `app/ml/train.py`: loads dataset, applies pipeline, trains TF-IDF + Logistic Regression, saves model and vectorizer artifacts via `joblib`
- Implemented `app/ml/predict.py`: loads saved artifacts and returns predicted category + confidence score for a given text
- Ran first model training against `customer_support_tickets.csv`
- Updated `run_pipeline` in `app/services/pipeline.py` to accept a `language` parameter (default: `"english"`), enabling future Portuguese support
- Created `docs/product-vision-pt.md` and `docs/product-vision-en.md`: complete product vision defining system flow, LLM layer, priority logic, human queue, agent interface, database structure, business model and deployment strategy
- Updated `docs/project-context.md`: expanded with full product definition, key decisions, complete development order with status, and timeline
- Updated `docs/ml-notes.md`: added confidence threshold, multi-message classification strategy (Approach A/B), and feedback loop
- Updated `docs/architecture.md`: expanded online flow, added database structure and full tech stack
- Updated `README.md`: updated system architecture, tech stack, and planned features to reflect full product vision

### Problems
- Dataset is synthetic: ticket descriptions have no clear semantic relationship with the labels, making it impossible to assess real model accuracy
- `predict.py` depends on artifacts existing — if `train.py` hasn't run yet, it would crash at import time

### Solutions
- `FileNotFoundError` caught at module load in `predict.py`: exits with a clear message instructing the user to run `train.py` first
- Dataset issue flagged for replacement — current results are not representative of real-world performance

### Learnings
- Learned the basics of TF-IDF vectorization and Logistic Regression in Scikit-learn
- Synthetic datasets can produce misleading metrics — data quality is critical before trusting any model evaluation
- Multilingual support requires separate models per language — a single model cannot handle both English and Portuguese reliably

### Next Steps
- Find a better (real) dataset to replace `customer_support_tickets.csv`
- Find a Portuguese dataset and train a separate Portuguese model to enable multilingual support

---

## 2026-04-09 (Lucas)

### What was done
- Created `tests/test_preprocessing.py`: pytest coverage for `clean_text` (lowercase, punctuation removal, whitespace normalization, empty input, accented characters preserved, non-string input)
- Created `tests/test_normalizer.py`: pytest coverage for `normalize_text` (stopword removal, empty input, non-string input)
- Created `tests/test_pipeline.py`: pytest coverage for `run_pipeline` (returns string, empty input, end-to-end clean + normalize, non-string input)
- Moved `test-plan.md` from `tests/` to `docs/test-plan.md` (aligned with README documentation index)
- Left `conftest.py` empty for now; `test_train.py` and `test_predict.py` reserved for next session

### Problems
- Some edge cases deliberately out of scope for MVP — not worth testing or handling yet

### Solutions
- Deferred those cases; focused tests on core behavior the pipeline must guarantee today

### Learnings
- Learned how to write and run pytest tests for the project

### Next Steps
- Finish remaining tests (`test_train.py`, `test_predict.py`, API layer when ready)
- Create retraining scripts (`scripts/retrain.py` per project context)

---

## 2026-04-10 (Lucas)

### What was done
- Extended `app/ml/train.py`: `train_model` now accepts explicit CSV column names (`texts`, `labels`), optional `model_path` / `vectorizer_path` for tests and alternate outputs; drops rows whose text becomes empty after `run_pipeline` before train/test split
- Added `app/core/config.py` constants `TEXT_COLUMN` and `LABEL_COLUMN` for the production dataset column names
- Added `app/ml/predict_category.py`: `predict_category` runs `run_pipeline` then inference; returns `{"category": "unknown", "score": 0.0}` when preprocessed text is blank (no artifact load); lazy-loads model and vectorizer with thread-safe caching; raises `FileNotFoundError` with clear paths if artifacts are missing
- Added `tests/fixtures/minimal_train.csv` and `tests/fixtures/empty_after_pipeline.csv` for deterministic training tests
- Expanded root `conftest.py`: fixtures `train_artifact_paths`, `minimal_train_csv`, `empty_after_pipeline_csv`, `patch_predict_category_artifacts` (monkeypatch paths + clear predict cache)
- Implemented `tests/test_train.py`: valid artifacts written, invalid column names raise `KeyError`, empty-after-pipeline rows raise `ValueError`
- Implemented `tests/test_predict.py`: empty string → `unknown` / `0.0`, trained model returns valid shape and score range, missing artifact files raise `FileNotFoundError`
- Added `tests/best_practices.md` — short guide on when and how to write tests in this repo
- `tests/test_api.py` remains a stub for FastAPI tests (next)

### Problems
- Tiny training fixture triggers sklearn `UndefinedMetricWarning` in `classification_report` when a label has no predicted samples in the test split — noisy but tests still pass
- Some Python syntax patterns were unfamiliar while implementing train/predict tests
- Pytest mechanics (`monkeypatch`, fixtures) not yet fully comfortable — need a focused review tomorrow to understand the test code end-to-end

### Solutions
- Documented in `docs/ml-notes.md` (sklearn warnings section); optional future fix: `zero_division` in `classification_report` or pytest `filterwarnings`
- Planned self-study on fixtures and `monkeypatch` before extending tests further

### Learnings
- Fixtures and `monkeypatch` keep ML tests isolated from real `artifacts/` paths (conceptually clear even if implementation details still being absorbed)
- Lazy loading + lock avoids reloading model on every prediction in production-style usage

### Next Steps
- *(Superseded 2026-04-11 — see entry below.)* Pipeline + prediction-model slice closed without DB persistence; optional operational `scripts/retrain.py` remains a future enhancement tied to the feedback loop.

---

## 2026-04-11 (Lucas)

### What was done
- **Closed MVP slice — pure pipeline + prediction model (Lucas):** preprocessing → `train_model` → `predict_category` → unit tests; **explicitly out of scope for this milestone:** persisting the ticket or prediction to the database after inference (that work stays with API + DB integration).
- Added `scripts/retest.bat` and `scripts/retest.ps1`: run `python -m pytest` from the repository root so root `conftest.py` and `tests/` resolve correctly; extra pytest args are forwarded.
- Added `scripts/retest.md`: usage, prerequisites, PowerShell execution policy, troubleshooting (`ModuleNotFoundError: app`, etc.).
- Added `scripts/best_practices.md`: conventions for scripts as thin wrappers over `app/` logic; links to retest docs.
- **PR:** documentation pass so reviewers see a consistent story for the ML/pipeline deliverable.

### Problems
- None blocking release of this slice.

### Solutions
- N/A

### Learnings
- Wrapper scripts reduce friction for contributors running tests from the wrong working directory.

### Next Steps
- Open PR and hand off to API/DB track (`FastAPI`, persistence, `test_api.py`).
- Later: operational retraining entry point (`scripts/retrain.py` or equivalent) when the feedback-loop milestone is scheduled.
