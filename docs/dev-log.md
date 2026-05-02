
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
- *(Superseded 2026-04-12 — see below.)* API technical MVP landed on `feature/api-mvp`; next is merge + DB/persistence track.

---

## 2026-04-12 (Lucas)

### What was done
- Documented **`feature/api-mvp` vs `develop`:** new file `docs/branch-feature-api-mvp-vs-develop.md` (routes, schemas, `limits`, training row filter, config env vars, `api-contracts` / `security-and-deployment`, `test_api`, deps)
- Updated **`docs/project-context.md`**, **`docs/ml-notes.md`**, **`docs/README.md`**, and **`README.md`** so the PR narrative matches: technical API MVP lives on `feature/api-mvp`; `develop` still has stub routes until merge
- Listed **what remains** after this PR: DB persistence, auth/rate limits, product channels, retrain automation, hardening (cross-ref `security-and-deployment.md`)
- Clarified **authorship:** the shipped technical MVP (including API) is **entirely Lucas**; **`docs/team-responsibilities.md`** updated so Salim / Rafael / Luís are framed as **future** ownership, not contributors to this MVP

### Problems
- None (documentation sync)

### Solutions
- N/A

### Learnings
- Keeping a short branch-delta doc avoids reviewers guessing what `develop` already had

### Next Steps
- Merge feature branches → `develop` when approved; refresh docs that mention stub routes vs merged code paths.

---

## 2026-04-13 (Lucas)

### What was done
- **Queue read API:** **`GET /tickets`** — query params **`queue_target`** (optional), **`limit`**, **`offset`**; ordering via **`list_tickets_queue`** (**HIGH** → **MEDIUM** → **LOW**, then **`created_at`** ASC); responses **`TicketQueueItem`** / **`TicketQueueResponse`**; errors **503** (no DB / query failure), **422** (invalid **`queue_target`**).
- **Tests:** **`tests/test_queue_api.py`**; root **`conftest.py`** — **`sqlite_session_factory`** shared with persistence-style overrides.
- **Docs sync:** **`README.md`** (features + MVP checklists), **`docs/architecture.md`** (queue read path), **`docs/ml-notes.md`**, **`docs/test-plan.md`** (§4.8), **`docs/branch-feature-api-mvp-vs-develop.md`**, **`docs/README.md`** index; cruzado com **`docs/project-context.md`**, **`docs/api-contracts.md`**, **`docs/security-and-deployment.md`**.

### Problems
- None blocking.

### Next Steps
- Ticket **detail** / **PATCH**, auth, and product schema for messages / agent replies.

---

## 2026-04-24 (Lucas)

### What was done
- **`feature/database` / persistence slice documented:** `app/db/` (SQLAlchemy `Ticket`, `get_db` + **`DATABASE_URL`**, `save_ticket_prediction`), **`classify_ticket`** facade, **`POST /predict`** requiring persistence (**503** if unset/failing commit).
- Docs synced: **`README.md`** (Data/API sections, setup step DB + `.env.example`, roadmap checkboxes), **`docs/architecture.md`** (persistence layer, `tickets` schema vs planned tables, critical path), **`docs/project-context.md`** (development order items 9–10), **`docs/branch-feature-api-mvp-vs-develop.md`** (persistence + deps rows), **`docs/security-and-deployment.md`** (**DATABASE_URL** notes), **`docs/api-contracts.md`** / **`docs/ml-notes.md`** / **`docs/test-plan.md`** nits.
- Added repo-root **`.env.example`** for onboarding.

### Problems
- `POST /predict` runs inference before failing when **`DATABASE_URL`** is missing — documented behavior (potential refactor later).

### Next Steps
- **Alembic** or more SQL migrations as schema grows; optional inference-before-DB reorder.

---

## 2026-05-02 (Lucas)

### What was done
- **Ticket triage:** `app/services/ticket_triage.py` (category → **`HIGH`/`MEDIUM`/`LOW`**, score → **`human`/`llm`**), `app/core/triage_settings.py` (**`SMARTTICKET_LLM_MIN_SCORE`**, clamp + safe parse).
- **API + DB:** `PredictResponse` and `Ticket` include **`urgency`** + **`queue_target`**; `POST /predict` persists both; `db/migrations/001_add_urgency_queue_target.sql` for existing PostgreSQL.
- **Tests:** `tests/test_ticket_triage.py`, `tests/test_triage_settings.py`; updates to `test_api` / `test_persistence`.
- **Docs:** `README` checklists + samples, `architecture.md`, `project-context.md` (technical MVP closure status), `api-contracts.md`, `ml-notes.md`, `security-and-deployment.md`, `test-plan.md`, `branch-feature-api-mvp-vs-develop.md`, `docs/README.md`.
- **Fecho do MVP técnico (âmbito *Technical MVP closure*):** marco considerado **concluído em 02/05/2026** — critérios da tabela de encerramento cumpridos no código (triage + persistência + **`GET /tickets`** + testes); referência de data alinhada em **`docs/project-context.md`**, **`README.md`** (Overview + checklist) e **`docs/README.md`**.

### Problems
- None blocking.

### Next Steps
- Ticket **detail** / **PATCH**, auth, extensões de **`GET /tickets`** conforme o produto (além do filtro **`queue_target`**); leitura de fila documentada na entrada **2026-04-13**.

---

