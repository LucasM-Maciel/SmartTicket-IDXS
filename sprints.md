# Sprint plan — SmartTicket-IDXS

> **Living document:** update checkboxes as work completes.  
> **As of 2026-05-02:** **technical MVP closure is complete** (see `docs/project-context.md`): `GET /health`, `POST /predict` + persistence (`DATABASE_URL`), triage (`urgency` / `queue_target`), `GET /tickets` (queue order + pagination/filter), tests and docs aligned.
> **Ownership note:** Sprint sections under each person reflect **planning/track ownership**, not code authorship. For shipped contributions/authorship, use `docs/team-responsibilities.md` and `docs/project-context.md`.

---

## Progress snapshot

| Phase | Status |
|-------|--------|
| Sprints 0–4 (foundation, pipeline, API + persistence) | **Done** (technical MVP closed) |
| Sprint 5 (LLM integration) | **Not started** (stub only) |
| Sprints 6+ (hardening, channels, product E2E) | **Planned / in progress by roadmap** |

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

### Rafael (track ownership)

- [x] Define categories (business + UX) — see product vision docs (`docs/product-vision-pt.md`, `docs/product-vision-en.md`)
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

### Salim (track ownership)

- [x] FastAPI project layout (`app/main.py`, `app/api/`) — **skeleton in place**
- [x] `POST /predict` + `GET /health` **implemented** and aligned with `docs/api-contracts.md`
- [x] Architecture baseline documented (`docs/architecture.md`, `docs/project-context.md`)

### Rafael (track ownership)

- [x] README / docs index improved over time
- [x] System overview in `docs/` (multiple files; no single `system-overview.md`)

### Luís (track ownership)

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

### Salim (track ownership)

- [ ] Integrate preprocessing **via** `predict_category` / API only (pipeline owned by Lucas — **no duplicate** `pipeline.py` under Salim)

### Rafael (track ownership)

- [x] Test scenarios / expected outputs (partially in tests + docs)

### Luís (track ownership)

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

### Rafael (track ownership)

- [x] Category validation examples (in docs / tests fixtures)

### Luís (track ownership)

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

### Salim (track ownership)

- [x] Wire `POST /predict` to `predict_category`
- [x] Pydantic schemas (`app/api/schemas.py`) aligned with `docs/api-contracts.md`
- [x] `GET /health`
- [x] `tests/test_api.py`
- [x] `GET /tickets` queue read (`queue_target`, `limit`, `offset`) + `tests/test_queue_api.py`

### Rafael (track ownership)

- [ ] API usage examples in README or `docs/` once routes exist

### Luís (track ownership)

- [ ] Integration test support (optional)

### Shared

- [x] End-to-end: HTTP → predict → response with DB persistence (`DATABASE_URL`) + triage fields

---

# Sprint 5 — LLM integration (optional)

**Duration:** 5–7 days

## Goal

Optional AI-generated responses (`app/services/llm_service.py`).

### Lucas

- [ ] LLM client + context from classification + fallback

### Salim (track ownership)

- [ ] LLM in API flow + feature toggle

### Rafael (track ownership)

- [ ] Prompt templates per category

### Luís (track ownership)

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

### Salim (track ownership)

- [ ] Error handling, API structure, DB integration complete

### Rafael (track ownership)

- [ ] Final user-facing docs

### Luís (track ownership)

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

### Salim (track ownership)

- [ ] Webhook endpoint, idempotency basics

### Lucas

- [ ] Real-time message shape compatibility with pipeline

### Rafael (track ownership)

- [ ] Chat-oriented response patterns

### Luís (track ownership)

- [ ] E2E debugging

### Shared

- [ ] WhatsApp → API → out validation

---

## Timeline (indicative)

| Sprint | Duration | Notes |
|--------|----------|--------|
| 0–2 | ~2–3 weeks | Mostly **done** |
| 3–4 | ~2 weeks | Training + API/persistence/triage/queue read **done** |
| 5–8 | Post-technical-MVP | LLM, hardening, WhatsApp, product E2E |

**Rule:** if blocked &gt; 1 day on non-critical path → simplify and ship the next increment.


---

# Functional MVP — Sprints F1–F6

> **Start:** May 2026
> **Target:** pilot client validation in ~6 weeks
> **Owner:** Lucas (solo development)
>
> **Confirmed decisions:**
> - Channel: **Z-API** (MVP) → Twilio/Meta Cloud API (next milestone)
> - Queue worker: **APScheduler** inside FastAPI (→ RabbitMQ when monolith splits into two APIs)
> - Hosting: **Railway** (stays; Pro plan US$20 sufficient for 1–3 pilot clients)
> - Attendant UI: **React + Next.js** (shadcn/ui, simple first, iterate later)
> - LLM: **OpenAI GPT-4o mini** (feature-toggled via `SMARTTICKET_LLM_ENABLED`)
> - Auth (pilot): NextAuth.js with credential provider (simple fixed users)

---

# Sprint F1 — Real dataset + PT-BR pipeline

**Duration:** 5–7 days

## Goal

Replace synthetic dataset with real/realistic PT-BR data and make the preprocessing pipeline language-aware.

### Lucas

- [ ] **Dataset generation:** use GPT-4o to generate PT-BR variations per category (10 seed examples per category → 50+ variations → manual review)
- [ ] **Dataset target:** ~400 examples minimum (80+ per category: `technical_issue`, `billing_inquiry`, `refund_request`, `cancellation_request`, `product_inquiry`)
- [ ] **PT-BR pipeline:** extend `normalize_text` to load `stopwords('portuguese')` when `language='pt'`; update `run_pipeline` to accept/pass `language` param; add `SMARTTICKET_PIPELINE_LANGUAGE` env var (default `'en'`)
- [ ] **NLTK bootstrap:** ensure `nltk_bootstrap.py` downloads stopwords for both `english` and `portuguese`
- [ ] Retrain model with new dataset and evaluate with `classification_report`
- [ ] Update `tests/test_normalizer.py` and `tests/test_pipeline.py` for PT-BR path
- [ ] Update `.env.example` with `SMARTTICKET_PIPELINE_LANGUAGE`

---

# Sprint F2 — DB schema + contacts/messages

**Duration:** 3–5 days

## Goal

Extend the database to support the full operational flow (contacts, messages, ticket status transitions).

### Lucas

- [ ] `contacts` table: `id` (UUID), `phone`, `name`, `channel`, `created_at`
- [ ] `messages` table: `id`, `contact_id`, `ticket_id`, `direction` (`inbound`/`outbound`), `body`, `external_id` (BSP message id), `created_at`
- [ ] Extend `tickets`: add `contact_id` (FK), `channel` (`whatsapp`/`api`), `status` transitions (`open` → `in_progress` → `resolved` / `escalated`)
- [ ] SQL migration `db/migrations/002_functional_mvp_schema.sql`
- [ ] SQLAlchemy models for `Contact` and `Message`
- [ ] Repositories: `contact_repository.py`, `message_repository.py`
- [ ] New API routes: `GET /tickets/{id}`, `PATCH /tickets/{id}` (status + urgency override), `POST /tickets/{id}/reply`
- [ ] Update `docs/architecture.md` with new schema

---

# Sprint F3 — WhatsApp channel (Z-API)

**Duration:** 5–7 days

## Goal

Receive and send WhatsApp messages via Z-API webhook.

### Lucas

- [ ] Webhook endpoint `POST /webhooks/whatsapp` with Z-API payload parsing
- [ ] Idempotency: skip if `external_id` already processed (deduplicate on `messages.external_id`)
- [ ] Extract contact (phone, name) → upsert `contacts`
- [ ] Extract message text → run `classify_ticket` → persist ticket + message
- [ ] Outbound: `app/services/channel/zapi_client.py` wrapping Z-API send-message HTTP call
- [ ] Abstract BSP interface `app/services/channel/base.py` (Twilio swap = new file only)
- [ ] Env vars: `ZAPI_INSTANCE_ID`, `ZAPI_TOKEN`, `ZAPI_BASE_URL` in `.env.example`
- [ ] Basic tests for webhook parsing and idempotency
- [ ] Channel provider swap via `SMARTTICKET_CHANNEL_PROVIDER` env var

---

# Sprint F4 — LLM integration + APScheduler worker

**Duration:** 5–7 days

## Goal

Wire LLM auto-response for high-confidence tickets and add the queue worker with priority aging.

### Lucas

- [ ] Complete `app/services/llm_service.py`: OpenAI GPT-4o mini with context injection (`raw_text + category + score + urgency`)
- [ ] Prompt templates per category (PT-BR) in `app/services/llm_prompts.py`
- [ ] Feature toggle: `SMARTTICKET_LLM_ENABLED` (default `false`); fallback to `human` queue on error
- [ ] Persist LLM response in `messages` table (direction `outbound`, source `llm`)
- [ ] Send LLM response via Z-API outbound
- [ ] **APScheduler worker** (inside FastAPI lifespan):
  - Interval: `SMARTTICKET_WORKER_INTERVAL_SECONDS` (default 30s)
  - Picks next `llm` queue ticket (HIGH → MEDIUM → LOW + FIFO)
  - Calls LLM → sends reply → marks `resolved` or escalates to `human` on failure
- [ ] **Priority aging job:** every hour, promotes `MEDIUM` tickets older than `SMARTTICKET_AGING_HOURS_MEDIUM` (default 4h) to `HIGH`
- [ ] Env vars: `OPENAI_API_KEY`, `SMARTTICKET_LLM_ENABLED`, `SMARTTICKET_WORKER_INTERVAL_SECONDS`, `SMARTTICKET_AGING_HOURS_MEDIUM`
- [ ] Tests for LLM service (mocked OpenAI), prompt rendering, aging logic

> **Future migration note:** APScheduler → RabbitMQ when splitting into Ingestion API + Query API. APScheduler cannot coordinate work across multiple processes; RabbitMQ becomes necessary at that point.

---

# Sprint F5 — Attendant UI (Next.js)

**Duration:** 7–10 days

## Goal

Functional attendant interface: queue view, ticket detail, reply, status management.

### Lucas

- [ ] Next.js project under `ui/` (App Router + TypeScript + Tailwind + shadcn/ui)
- [ ] Auth: NextAuth.js with credentials provider (env-configured pilot users)
- [ ] **Queue page** (`/queue`): tickets ordered by urgency, urgency + queue_target badges, polling every 10s
- [ ] **Ticket detail** (`/tickets/[id]`): full conversation history, ticket metadata, LLM suggestion if available
- [ ] **Reply action:** text input → `POST /tickets/{id}/reply` → UI update
- [ ] **Status actions:** resolve, escalate, urgency override buttons
- [ ] **Filter bar:** urgency, queue_target, status
- [ ] Deploy to Railway as separate service; env `NEXT_PUBLIC_API_BASE_URL`
- [ ] `ui/README.md` with local setup instructions

---

# Sprint F6 — E2E integration + pilot handoff

**Duration:** 4–5 days

## Goal

Full flow validated end-to-end, pilot client onboarded.

### Lucas

- [ ] E2E smoke: WhatsApp message → webhook → classify → LLM reply → attendant sees in UI
- [ ] Tune `SMARTTICKET_LLM_MIN_SCORE` and urgency mapping based on real data
- [ ] `Dockerfile` for API + `ui/Dockerfile` for Next.js
- [ ] `docker-compose.yml` for local dev (API + Postgres + UI)
- [ ] Railway: two services (API + UI) sharing the same Postgres
- [ ] Sentry free tier for error tracking on both services
- [ ] Pilot client handoff: Z-API number configured, credentials, first real tickets flowing
- [ ] Update `docs/project-context.md` and `README.md` marking Functional MVP closed

---

## Functional MVP Timeline

| Sprint | Duration | Deliverable |
|--------|----------|-------------|
| F1 | Week 1 | PT-BR pipeline + real dataset + retrained model |
| F2 | Week 1–2 | DB schema (contacts, messages, ticket status) + new API routes |
| F3 | Week 2–3 | WhatsApp webhook (Z-API) inbound + outbound |
| F4 | Week 3–4 | LLM integration + APScheduler worker + priority aging |
| F5 | Week 4–5 | Next.js attendant UI (queue + detail + reply) |
| F6 | Week 5–6 | E2E validation + Docker + Railway deploy + pilot handoff |

---

## Post-Functional MVP (next milestone)

- Swap Z-API → Twilio / Meta Cloud API
- APScheduler → RabbitMQ (trigger: split monolith into Ingestion API + Query API)
- Next.js UI iteration (WebSocket real-time, analytics dashboard)
- Feedback loop: agent corrections feed model retraining
- Multi-client support (per-client category config + model artifacts)
