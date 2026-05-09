# SmartTicket — Functional MVP Plan

> Last updated: 2026-05-08  
> Status: **Planning** · Target: ~6 weeks from May 2026  
> Owner: Lucas Marques Maciel (solo development)  
> PDF export: [`docs/smartticket-functional-mvp-plan.html`](smartticket-functional-mvp-plan.html)

---

## Current state (Technical MVP — closed 02/05/2026)

The Technical MVP was built entirely by Lucas in approximately one month. Delivered:

| Component | What was delivered | Status |
|---|---|---|
| NLP pipeline | `clean_text` → `normalize_text` → `run_pipeline` | ✅ Done |
| ML model | TF-IDF + Logistic Regression, train + inference, `joblib` artifacts | ✅ Done |
| FastAPI | `GET /health`, `POST /predict`, `GET /tickets` | ✅ Done |
| Persistence | PostgreSQL via SQLAlchemy, `tickets` table | ✅ Done |
| Triage | Urgency (`HIGH`/`MEDIUM`/`LOW`) + routing (`human`/`llm`) | ✅ Done |
| Queue read | Ordered by urgency + FIFO, pagination, filters | ✅ Done |
| Tests | ~50 automated tests (unit + integration) | ✅ Done |
| Demo | Public Streamlit on Railway | ✅ Done |
| WhatsApp channel | — | ⏳ Pending |
| LLM (auto-reply) | Stub in `llm_service.py`, not integrated | ⏳ Pending |
| Attendant interface | — | ⏳ Pending |
| Queue worker | — | ⏳ Pending |

What the Functional MVP adds: real WhatsApp channel, LLM auto-reply, operational queue worker, attendant UI, and full contacts/messages schema.

---

## Confirmed decisions

| Decision | Choice | When to revisit |
|---|---|---|
| WhatsApp channel | **Meta Cloud API** (MVP and final product baseline) | Revisit only if provider constraints appear |
| Queue processing | **SQS + Lambda** for LLM queue; **PostgreSQL + APScheduler** for human queue (`queue_control`) | Revisit when aging moves to dedicated cron/job service |
| Hosting | **Railway Pro** (US$20/month) | Reassess when monthly cost exceeds US$40–50 or 5+ concurrent clients |
| Attendant UI | **React + Next.js** (App Router) | Iterate on top, never rewrite |
| LLM provider | **OpenAI GPT-4o mini** | Reassess cost/quality with real production data |
| Auth (pilot) | **NextAuth.js** — credentials provider | OAuth / SSO for final product |
| Pipeline language | **PT-BR** from F1 onwards | Multilingual when international clients arrive |
| Error tracking | **Sentry** free tier | Upgrade plan when client SLA requires it |

### Meta Cloud API decision (MVP + final baseline)

| Decision factor | Meta Cloud API choice |
|---|---|
| Cost model | Pay-as-you-go (Meta conversation/template billing), no mandatory BSP subscription |
| Channel trust | Official Meta stack, stronger commercial positioning with clients |
| Bureaucracy | Requires Meta Business setup/verification and webhook verification flow |
| Operational risk | Lower block risk versus unofficial providers |
| Product fit | Better long-term baseline for MVP functional + final product |
| Recommendation | Start directly with Meta Cloud API and keep provider abstraction in code |

**Implementation path:** use a provider adapter (`app/services/channel/base.py` + `meta_client.py`) so fallback providers remain possible without rewriting domain logic.

### Queue architecture decision (LLM queue vs human queue)

LLM queue will use **SQS + Lambda** (event-driven). Human queue remains in **PostgreSQL + APScheduler**, controlled by `queue_control` and urgency rules.

Current split rationale:
- LLM processing benefits from event-driven fan-out and retry semantics (SQS + Lambda)
- Human queue keeps deterministic business ordering in SQL (HIGH → MEDIUM → LOW + FIFO)
- `queue_control` keeps operational state transitions explicit (`human_queue` / `llm_queue`)
- Aging stays in human queue logic; may move from APScheduler to dedicated cron/job service later

Decision: for final-product direction (for now), do **not** adopt RabbitMQ; use SQS + Lambda for LLM queue and keep human queue in PostgreSQL + APScheduler/cron with `queue_control`.

---

## Sprint plan — 6 weeks

---

### Sprint F1 — Real dataset + PT-BR pipeline

**Duration:** 5–7 days · Week 1  
**Why first:** the model is trained on synthetic English data. A poor model misclassifies, misroutes, generates wrong LLM replies, and destroys pilot client trust. Fix before any integration.

#### Dataset

- [ ] Generate PT-BR dataset with GPT-4o: 10 seed examples per category → 50+ generated variations → manual review
- [ ] Target: 400+ total examples, 80+ per category (`technical_issue`, `billing_inquiry`, `refund_request`, `cancellation_request`, `product_inquiry`)
- [ ] Verify class balance and remove duplicates

#### PT-BR pipeline

- [ ] Extend `normalize_text` to accept `language='pt'` and load `stopwords('portuguese')`
- [ ] Update `run_pipeline` to accept and pass `language` parameter
- [ ] Add env var `SMARTTICKET_PIPELINE_LANGUAGE` (default `'en'`) to `app/core/config.py`
- [ ] Ensure `nltk_bootstrap.py` downloads stopwords for both `english` and `portuguese`

#### Model + Tests

- [ ] Retrain with `python -m app.ml.train` and validate `classification_report`
- [ ] Update `tests/test_normalizer.py` and `tests/test_pipeline.py` to cover PT-BR path
- [ ] Update `.env.example` with `SMARTTICKET_PIPELINE_LANGUAGE`

**Exit criterion:** model trained on PT-BR with acceptable accuracy across 5 categories, all tests passing.

---

### Sprint F2 — DB schema + contacts/messages + new API routes

**Duration:** 3–5 days · Week 1–2  
**Why before WhatsApp:** the webhook needs to save contact and message. Better to have the schema ready and tested before integrating the channel.

#### Database — new tables

- [ ] `contacts` table: `id` (UUID), `phone`, `name`, `channel`, `created_at`
- [ ] `messages` table: `id`, `contact_id`, `ticket_id`, `direction` (`inbound`/`outbound`), `body`, `external_id` (BSP message id), `created_at`
- [ ] Extend `tickets`: add `contact_id` (FK), `channel` (`whatsapp`/`api`), `queue_control` (`human_queue`/`llm_queue`), `status` transitions (`open` → `in_progress` → `resolved`/`escalated`)
- [ ] SQL migration: `db/migrations/002_functional_mvp_schema.sql`

#### SQLAlchemy + Repositories

- [ ] SQLAlchemy models: `Contact` and `Message` in `app/db/models.py`
- [ ] `contact_repository.py`: upsert by phone
- [ ] `message_repository.py`: insert, list by ticket

#### New API routes

- [ ] `GET /tickets/{id}` — ticket detail with messages
- [ ] `PATCH /tickets/{id}` — update status and/or urgency override
- [ ] `POST /tickets/{id}/reply` — attendant sends reply (persists + dispatches via channel)
- [ ] `GET /contacts/{id}/tickets` — contact ticket history
- [ ] Update `docs/architecture.md` and `docs/api-contracts.md`

**Exit criterion:** migration applied, models created, routes working with tests.

---

### Sprint F3 — WhatsApp channel (Meta Cloud API)

**Duration:** 5–7 days · Week 2–3

#### Inbound (receive messages)

- [ ] Endpoint `POST /webhooks/whatsapp` with Meta Cloud API payload parsing
- [ ] Idempotency: check if `external_id` already exists in `messages` before processing (prevents duplicate retries)
- [ ] Extract contact (phone, name) → upsert `contacts`
- [ ] Extract message text → run `classify_ticket` → persist ticket + message (inbound)

#### Outbound (send messages)

- [ ] `app/services/channel/meta_client.py`: wraps Meta Cloud API send-message HTTP call
- [ ] Abstract interface `app/services/channel/base.py` with `send_message(phone, text)` method — provider adapter stays isolated
- [ ] Webhook verification challenge + token validation

#### Config + Tests

- [ ] Env vars: `META_WA_PHONE_NUMBER_ID`, `META_WA_ACCESS_TOKEN`, `META_WA_VERIFY_TOKEN`, `META_WA_API_VERSION` in `.env.example`
- [ ] Tests: webhook parsing, idempotency logic, mocked outbound HTTP

> **Fallback option:** keep provider abstraction so Z-API/Twilio adapters can be added later only if needed.

**Exit criterion:** WhatsApp message → classified ticket in the database.

---

### Sprint F4 — LLM integration + APScheduler worker + priority aging

**Duration:** 5–7 days · Week 3–4

#### LLM Integration (OpenAI GPT-4o mini)

- [ ] Complete `app/services/llm_service.py`: OpenAI client with context injection (`raw_text` + `category` + `score` + `urgency`)
- [ ] PT-BR prompt templates per category in `app/services/llm_prompts.py`
- [ ] Feature toggle: `SMARTTICKET_LLM_ENABLED` (default `false`); fallback to `human` queue on LLM error
- [ ] LLM response persisted in `messages` (direction `outbound`, source `llm`)
- [ ] Send response via Meta Cloud API outbound

#### APScheduler Worker (inside FastAPI lifespan)

- [ ] Worker interval: `SMARTTICKET_WORKER_INTERVAL_SECONDS` (default 30s)
- [ ] Logic: pick next ticket with `queue_target: llm` and `status: open` in order HIGH → MEDIUM → LOW + FIFO
- [ ] Flow: call LLM → send reply → mark ticket `resolved`
- [ ] Fallback: LLM error → escalate to human queue (`queue_target: human`, `status: open`)

#### Priority Aging

- [ ] Separate APScheduler job running every 1 hour
- [ ] Promotes `MEDIUM` + `status: open` tickets older than `SMARTTICKET_AGING_HOURS_MEDIUM` hours (default 4h) to `HIGH`
- [ ] Logs each promotion

#### Env vars + Tests

- [ ] Env vars: `OPENAI_API_KEY`, `SMARTTICKET_LLM_ENABLED`, `SMARTTICKET_WORKER_INTERVAL_SECONDS`, `SMARTTICKET_AGING_HOURS_MEDIUM`
- [ ] Tests: LLM service (mocked OpenAI), prompt rendering, aging logic

> **Queue evolution note:** final direction is SQS + Lambda for LLM queue; human queue remains PostgreSQL + APScheduler (or dedicated cron/job service) using `queue_control`.

**Exit criterion:** full LLM path end-to-end working with feature toggle.

---

### Sprint F5 — Attendant UI (Next.js)

**Duration:** 7–10 days · Week 4–5  
**Stack:** Next.js App Router + TypeScript + Tailwind CSS + shadcn/ui  
**Auth:** NextAuth.js with credentials provider (env-configured users for pilot)

#### Setup

- [ ] Next.js project under `ui/` with App Router, TypeScript, Tailwind, shadcn/ui
- [ ] NextAuth.js with credentials provider

#### Queue page (`/queue`)

- [ ] Ticket table ordered by urgency (HIGH first)
- [ ] Urgency badges (red/yellow/green) and `queue_target` (human/LLM)
- [ ] Auto-refresh via polling every 10s
- [ ] Filter bar: urgency, `queue_target`, status

#### Ticket detail page (`/tickets/[id]`)

- [ ] Full conversation history (inbound/outbound messages with timestamp and source)
- [ ] Ticket metadata: category, score, urgency, `queue_target`
- [ ] LLM suggestion (if available)
- [ ] Manual urgency override button

#### Attendant actions

- [ ] Text input → `POST /tickets/{id}/reply` → optimistic UI update
- [ ] "Resolve" and "Escalate" buttons with confirmation

#### Deploy

- [ ] Deploy to Railway as separate service with `NEXT_PUBLIC_API_BASE_URL`
- [ ] `ui/README.md` with local setup and env vars

**Exit criterion:** attendant can see queue, open ticket, read history, reply. Reply appears on client's WhatsApp.

---

### Sprint F6 — E2E integration + pilot handoff

**Duration:** 4–5 days · Week 5–6

#### E2E Validation

- [ ] Full smoke test: WhatsApp message → webhook → classify → LLM reply (if enabled) → attendant sees in UI → reply back to WhatsApp
- [ ] Tune `SMARTTICKET_LLM_MIN_SCORE` and urgency mapping based on real data behavior

#### Docker

- [ ] `Dockerfile` for the API
- [ ] `ui/Dockerfile` for Next.js
- [ ] `docker-compose.yml` for local dev (API + Postgres + UI)

#### Railway + Monitoring

- [ ] Railway: two services (API + UI) sharing the same Postgres
- [ ] Sentry free tier integrated on both services

#### Pilot handoff

- [ ] Meta phone number configured on production environment
- [ ] Attendant credentials created and delivered
- [ ] First real tickets flowing and being processed
- [ ] Update `docs/project-context.md` and `README.md` marking Functional MVP closed

**Exit criterion:** pilot client operating with real tickets.

---

## Timeline summary

| Sprint | Duration | Deliverable |
|--------|----------|-------------|
| F1 | Week 1 | PT-BR pipeline + real dataset + retrained model |
| F2 | Week 1–2 | DB schema (contacts, messages, ticket status + `queue_control`) + new API routes |
| F3 | Week 2–3 | WhatsApp webhook (Meta Cloud API) inbound + outbound |
| F4 | Week 3–4 | LLM integration + APScheduler worker + priority aging |
| F5 | Week 4–5 | Next.js attendant UI (queue + detail + reply) |
| F6 | Week 5–6 | E2E validation + Docker + Railway deploy + pilot handoff |

---

## Environment variables — full reference

| Variable | Default | Sprint | Description |
|---|---|---|---|
| `DATABASE_URL` | — | Technical | PostgreSQL URL (required) |
| `SMARTTICKET_LLM_MIN_SCORE` | `0.75` | Technical | Min score for LLM routing |
| `SMARTTICKET_DISABLE_OPENAPI` | `false` | Technical | Hide /docs and /redoc in production |
| `SMARTTICKET_PIPELINE_LANGUAGE` | `en` | F1 | NLP pipeline language (`pt` for PT-BR) |
| `META_WA_PHONE_NUMBER_ID` | — | F3 | Meta WhatsApp phone number ID |
| `META_WA_ACCESS_TOKEN` | — | F3 | Meta Cloud API access token |
| `META_WA_VERIFY_TOKEN` | — | F3 | Webhook verification token |
| `META_WA_API_VERSION` | `v20.0` | F3 | Meta Graph API version for WhatsApp endpoints |
| `OPENAI_API_KEY` | — | F4 | OpenAI API key |
| `SMARTTICKET_LLM_ENABLED` | `false` | F4 | Enable LLM auto-reply path |
| `SMARTTICKET_WORKER_INTERVAL_SECONDS` | `30` | F4 | APScheduler worker interval |
| `SMARTTICKET_AGING_HOURS_MEDIUM` | `4` | F4 | Hours before MEDIUM promotes to HIGH |
| `NEXT_PUBLIC_API_BASE_URL` | — | F5 | API URL for the Next.js frontend |

---

## Post-Functional MVP — next milestone

| Item | Trigger | Impact |
|---|---|---|
| Keep Meta Cloud API as baseline | Continuous | Official channel positioning and lower long-term operational risk |
| SQS + Lambda for LLM queue (no RabbitMQ) | During split to Ingestion + Query API | Event-driven scaling and retry semantics for LLM workload |
| Next.js UI iteration | After pilot feedback | WebSocket real-time, analytics dashboard, better UX |
| Feedback loop | When 200+ real corrected tickets exist | Agent corrections feed model retraining |
| Multi-client support | When 2+ paying clients | Per-client category config + model artifacts |
| Human queue stays SQL-driven (`queue_control` + APScheduler/cron) | During and after split | Preserves deterministic business priority and aging logic |
