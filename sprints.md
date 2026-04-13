# Sprint plan — SmartTicket-IDXS

> **Living document:** update checkboxes as work completes.  
> **As of 2026-04-12:** offline **pipeline + training + `predict_category` + ML unit tests** slice is done (see `docs/project-context.md`). **Next focus:** FastAPI, persistence, API tests (Salim track).

---

## Progress snapshot

| Phase | Status |
|-------|--------|
| Sprints 0–3 (data, pipeline, training) | Largely **done** |
| Sprint 4 (inference in API) | **Partial** — ML ready; HTTP routes still to wire |
| Sprints 5+ (LLM, WhatsApp, hardening) | **Not started** (post-MVP / optional) |

---

# Sprint 0 — Dataset & problem definition

**Duration:** 3–5 days

## Goal

Define classification problem and initial dataset.

### Lucas

- [x] Find or create dataset (synthetic CSV in repo; replace with real data later)
- [x] Analyze data quality (ongoing; documented in `docs/ml-notes.md`)
- [x] Identify noise / limitations (noted for synthetic data)
- [x] Validate usability for baseline model

### Rafael

- [x] Define categories (business + UX) — see `docs/reuniao-regras-negocio.md` / vision docs
- [x] Create examples per category (evolving)

### Shared

- [x] Align classification scope
- [x] Define initial labels (MVP category set in docs)

---

# Sprint 1 — Foundation & setup

**Duration:** 3–5 days

## Goal

Project structure, environment, app shell.

### Lucas

- [x] Project structure (`app/utils`, `app/ml`, `app/services`, …)
- [x] Initial text cleaning / normalization (`clean_text`, `normalize_text`)
- [x] Preprocessing steps defined and tested

### Salim

- [x] FastAPI project layout (`app/main.py`, `app/api/`) — **skeleton in place**
- [ ] `POST /predict` + `POST /health` **implemented** and aligned with `docs/api-contracts.md`
- [x] Architecture baseline documented (`docs/architecture.md`, `docs/project-context.md`)

### Rafael

- [x] README / docs index improved over time
- [x] System overview in `docs/` (multiple files; no single `system-overview.md`)

### Luís

- [ ] Structure review (as needed)

### Shared

- [x] MVP scope aligned (full product MVP vs technical slice in `project-context.md`)

---

# Sprint 2 — Data pipeline & preprocessing

**Duration:** 5–7 days

## Goal

Reliable reusable text preprocessing.

### Lucas

- [x] Full preprocessing pipeline (`run_pipeline` in `app/services/pipeline.py`)
- [x] Normalization + stopwords (`app/utils/`)
- [x] Reusable utilities + pytest (`tests/test_preprocessing.py`, `test_pipeline.py`, …)

### Salim

- [ ] Integrate preprocessing **via** `predict_category` / API only (pipeline owned by Lucas — **no duplicate** `pipeline.py` under Salim)

### Rafael

- [x] Test scenarios / expected outputs (partially in tests + docs)

### Luís

- [ ] Preprocessing review / perf (optional)

### Shared

- [x] Preprocessing quality validated in tests

---

# Sprint 3 — ML model (training)

**Duration:** 4–6 days

## Goal

Train and persist classification model.

### Lucas

- [x] TF-IDF + Logistic Regression (`app/ml/train.py`)
- [x] Train/val split, `classification_report`, artifacts (`joblib`)
- [x] Configurable columns/paths (`app/core/config.py`)

### Rafael

- [x] Category validation examples (in docs / tests fixtures)

### Luís

- [ ] Model output review (optional)

### Shared

- [x] Baseline performance accepted for synthetic data (real eval later)

---

# Sprint 4 — ML integration (inference)

**Duration:** 4–6 days

## Goal

Expose classification through the API.

### Lucas

- [x] Prediction API in code: `predict_category` (`app/ml/predict_category.py`)
- [x] Lazy load + thread-safe cache, edge cases (`unknown` / missing artifacts)
- [x] ML tests (`tests/test_predict.py`, fixtures, `conftest.py`)

### Salim

- [ ] Wire `POST /predict` to `predict_category`
- [ ] Pydantic schemas (`app/api/schemas.py`) = `docs/api-contracts.md`
- [ ] `POST /health`
- [ ] `tests/test_api.py`

### Rafael

- [ ] API usage examples in README or `docs/` once routes exist

### Luís

- [ ] Integration test support (optional)

### Shared

- [ ] End-to-end: HTTP → predict → response (DB persistence = next step)

---

# Sprint 5 — LLM integration (optional)

**Duration:** 5–7 days

## Goal

Optional AI-generated responses (`app/services/llm_service.py`).

### Lucas

- [ ] LLM client + context from classification + fallback

### Salim

- [ ] LLM in API flow + feature toggle

### Rafael

- [ ] Prompt templates per category

### Luís

- [ ] Review latency / cost

### Shared

- [ ] Validate response quality

---

# Sprint 6 — Refinement & stability

**Duration:** 6–8 days

## Goal

Hardening before wider release.

### Lucas

- [ ] Model / edge-case improvements

### Salim

- [ ] Error handling, API structure, DB integration complete

### Rafael

- [ ] Final user-facing docs

### Luís

- [ ] Refactor / maintainability

### Shared

- [ ] Full regression testing + MVP sign-off

---

# Sprint 7 — Enhancements (optional)

**Duration:** 5–7 days

- [ ] Structured logging
- [ ] Confidence thresholds / routing rules
- [ ] Monitoring hooks
- [ ] Deployment checklist

---

# Sprint 8 — WhatsApp (business layer)

**Duration:** 5–7 days

## Goal

Real channel: WhatsApp → API → response.

### Salim

- [ ] Webhook endpoint, idempotency basics

### Lucas

- [ ] Real-time message shape compatibility with pipeline

### Rafael

- [ ] Chat-oriented response patterns

### Luís

- [ ] E2E debugging

### Shared

- [ ] WhatsApp → API → out validation

---

## Timeline (indicative)

| Sprint | Duration | Notes |
|--------|----------|--------|
| 0–2 | ~2–3 weeks | Mostly **done** |
| 3–4 | ~2 weeks | Training **done**; API wiring **in progress** |
| 5–8 | Optional / post-MVP | LLM, polish, WhatsApp |

**Rule:** if blocked &gt; 1 day on non-critical path → simplify and ship the next increment.
