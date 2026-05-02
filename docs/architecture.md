# System Architecture

> Last updated: 2026-04-25

## Overview

The system follows a layered architecture:

- **API layer** — HTTP requests, validation, classification orchestration, **DB writes on `POST /predict`** when configured
- **Service layer** — `classify_ticket` (typed facade over ML), `run_pipeline`
- **ML layer** — training (`train_model`) and inference (`predict_category`)
- **Persistence layer** — SQLAlchemy models and repositories (`app/db/`)
- **Utils layer** — text cleaning and normalization
- **Data layer** — datasets (CSV), relational DB (PostgreSQL), model artifacts (`.pkl`)

---

## MVP shape: modular monolith → two APIs (evolution)

**MVP (this phase):** one **modular monolith** — a single FastAPI deployable with **clear internal boundaries**:

- **Ingestion & processing** — channels/webhooks, validation, pipeline + ML orchestration, writes to the database, optional enqueue for heavy work later.
- **Query & attendant workflows** — list/detail tickets, statuses, and manual actions driven primarily by **reads and simple writes** to the same database.

Routers and services should reflect those boundaries (e.g. separate route modules and service entrypoints) so the codebase can later be split **without** a rewrite.

**Post-MVP target:** **two deployables** — an **ingestion API** (orchestrates intake + ML + persistence) and a **query API** (read-optimized, attendant/UI-facing), each with its own scaling and deploy lifecycle. The trigger for the split is documented in [`docs/adr/0001-mvp-modular-monolith-and-evolution-to-two-apis.md`](adr/0001-mvp-modular-monolith-and-evolution-to-two-apis.md).

---

## How we document architecture (design conventions)

- **C4 level 1 (context)** — SmartTicket, actors, and external systems (WhatsApp, LLM providers, DB host).
- **C4 level 2 (containers)** — FastAPI app(s), relational DB, and **candidate** containers (e.g. blob store for models, queue, cache) only after they appear in an ADR.
- **Sequence diagrams** — at least the critical path: request → predict → persist → response.
- **ADRs** — when the team **commits** to something (replica count, tenancy, Redis, where blobs live, **splitting ingest vs query**), record it under `docs/adr/`; until then, treat options below as **working assumptions**, not contracts.

Diagrams may live in draw.io / Mermaid / Excalidraw; this file stays the narrative anchor.

**Working Excalidraw (team):** [`docs/design system SmartTicket.excalidraw`](design%20system%20SmartTicket.excalidraw) — open in Cursor/VS Code with the Excalidraw extension (otherwise the file is JSON).

### Excalidraw in the browser (zoom, pan, edit)

GitHub does not run the Excalidraw canvas in the README. For the same experience as in the app, use a **Share** link from Excalidraw, or a **`.excalidraw`** file in the repo — see [docs/diagrams/README.md](diagrams/README.md).

**One-click link** (Excalidraw Share — zoom, pan in the browser):  
[Open architecture diagram in Excalidraw](https://excalidraw.com/#json=k3_Yr1wSJcZPRq9Y31wAc,umtchKOdn_ai6EmrwDaEew)

> **Tip:** after the canvas opens, switch Excalidraw to **dark mode** (sun/moon icon in the toolbar, or **Menu** → theme) for better contrast and readability of this diagram.

**Source in repo (optional, for diffs/PRs):** add [docs/diagrams/architecture.excalidraw](diagrams/architecture.excalidraw) when you export it, and keep it in sync; viewers can **Open** the file in [excalidraw.com](https://excalidraw.com) after download.

---

## Diagrams & build context (MVP → production)

Use this section as **shared context** when implementing or extending diagrams. It aligns drawing choices with the modular-monolith MVP and documented evolution.

### Two diagram “modes”

| Mode | Purpose | Typical inputs |
|------|---------|----------------|
| **Technical MVP** | Validate core path: pipeline, model, persistence, priority ordering | Synthetic / test dataset → API (no WhatsApp on the same canvas unless cramped) |
| **Product MVP** | End-to-end product story | WhatsApp / BSP → webhook → API → … → DB; **outbound** API → BSP → customer; attendant UI ↔ API |

Both modes still show **one deployable API** (modular monolith). Optional **sub-boxes or notes** inside the API (“ingestion vs query modules”) clarify future split **without** drawing two separate APIs until the team follows [`docs/adr/0001-mvp-modular-monolith-and-evolution-to-two-apis.md`](adr/0001-mvp-modular-monolith-and-evolution-to-two-apis.md).

### Critical path (`POST /predict` — as implemented)

```text
HTTP POST /predict
→ Pydantic validation (PredictRequest)
→ classify_ticket(text) → predict_category → category + score + text_processed
→ triage_prediction(category, score, llm_min_score=get_llm_min_score()) → urgency + queue_target
→ save_ticket_prediction(...) → INSERT INTO tickets
→ commit
→ PredictResponse JSON
```

**Dependency injection:** `get_db()` yields a SQLAlchemy `Session` when **`DATABASE_URL`** is set; otherwise **`None`**. After **`classify_ticket`** completes, if there is no session the handler returns **503** (`Database persistence not configured.`) — so inference runs even when persistence is off (consider reordering in a future refactor if you want to skip model load). Tests override `get_db` or use SQLite (`tests/test_persistence.py`). Root **`conftest.py`** clears `DATABASE_URL` during pytest so local `.env` never leaks into CI-style runs.

---

- **Solid boxes** — services **you** deploy and operate (FastAPI app, UI host, etc.).
- **Dashed boxes** — **external** providers (BSP / WhatsApp Cloud, LLM vendor) **or** a **thin internal HTTP client** (“API LLM” adapter) that only talks outbound; label the legend so readers are not confused by adapters sitting *inside* the environment boundary.

### WhatsApp / webhook path

- **Inbound:** BSP / channel provider → **HTTPS webhook** → **load balancer or edge** (if used) → **API SmartTicket**. Webhooks hit **your** URL; they do not write to the DB directly.
- **Outbound:** **API** → provider **send-message** API → WhatsApp → user. Omitting outbound arrows makes the architecture look ingestion-only.
- Optional labels on **user ↔ BSP** arrows (e.g. user message vs delivery/status) improve readability.

### Cloud, Docker, database, secrets

- **Cloud (dashed outer frame)** — everything running in **your** cloud account: edge/LB, compute, managed DB, UI if hosted there. **Actors** (customer, attendant browser) and **third-party** APIs stay **outside** that frame unless you deliberately draw a different convention (then add a one-line legend).
- **Docker** — represent as “API runs in container(s)”; **database** is usually **managed Postgres** and **not** in the same container as the app. Keep DB **inside** the cloud frame but **outside** the “app container” grouping.
- **Secrets** — not a user-data flow; show as **env / Secret Manager** injected at runtime (note or small dashed box → API or container), not as a parallel business pipeline.

### Priority queue vs message broker

- **“Priority queue”** in diagrams means the **product** queue: ordering / aging (see **Scheduled jobs** in Tech stack). **Baseline MVP does not assume RabbitMQ** (or any broker); introducing one is an **ADR** if the team needs async workers, multiple consumers, or cross-service buffering.
- If the drawing looks like a broker, add a caption: **logical queue (Postgres + scheduler)** unless an ADR says otherwise.

### Evolving to two APIs

If ingestion and query modules stay **bounded** (routers, services, minimal cross-calls), splitting into **two deployables** is **mostly mechanical** in code but adds **operational** work (two releases, auth between services if needed, clear DB write ownership). It is **not** a full rewrite when boundaries are clean; cost is often **ops + contracts**, not folder shuffling.

---

## Availability and deployment

**In code today:** `predict_category` keeps the loaded model and vectorizer **in memory inside each API process** (lazy load + lock). That is **not** Redis — it is per-process Python cache.

**Working targets (validate with the team before treating as fixed):**

| Phase | API instances | Load balancing | Notes |
|-------|---------------|----------------|--------|
| **MVP** | **1** | Usually none as a separate product — single endpoint from host/PaaS | Deploy may imply a short blip unless the platform does rolling updates. |
| **Production v1 (discussion)** | **2+** | **Some form of** traffic distribution + health checks (vendor ALB/NLB or managed equivalent) | Needs **stateless** HTTP layer; each replica still has its **own** in-memory model cache unless you later introduce a shared cache (that would be an explicit ADR). |

**Failure modes to plan for** (design-time checklist): deploy replacing the only task, process crash/OOM, DB unreachable, pool exhaustion, slow dependencies (e.g. LLM when added), TLS/cert issues, provider maintenance.

**Inference latency:** TF-IDF + logistic regression is usually cheap; cold start may pay **disk load** of `.pkl` on first use per process — define p50/p95 targets when `/predict` exists.

**Redis (or any shared cache):** **not assumed.** If multi-replica deployments need shared session/cache/queue, that is a **separate decision** — document pros/cons in an ADR; the baseline architecture does **not** require it for the current sklearn inference path.

---

## Tenancy and customization (under discussion)

Product direction includes **per-client categories and models**; **how** isolation is drawn is still architecture work:

- **Application:** a **single codebase** serving multiple clients is the default SaaS shape; **separate deploy per client** is a heavier enterprise pattern — choose explicitly if needed.
- **Data plane:** options include shared DB with tenant key vs **dedicated database per client** (commercial/ops trade-off). **No provider is fixed** (self-hosted Postgres, RDS, Neon, Supabase-as-Postgres-host, etc.) until documented in an ADR.
- **Model artifacts:** MVP can stay on **filesystem paths** (as today); **large-scale or multi-tenant blob storage** (S3-compatible, etc.) is a **likely evolution**, not a commitment in this file. Prefer **metadata in SQL, blobs in object storage** when you outgrow local disks — again, confirm in an ADR.

---

## Security and configuration (summary)

- **HTTPS** for public API traffic; terminate TLS at the edge (load balancer, reverse proxy, or PaaS).
- **Secrets and URLs** via **environment variables** (12-factor); never commit production secrets.
- **Logs:** structured JSON in production; avoid logging full ticket bodies by default; use correlation IDs per request.
- **Auth:** use mature libraries (FastAPI security utilities, JWT/API keys); validate third-party webhooks with provider signatures.

---

## Online flow (production target — product narrative)

```text
Customer sends message on WhatsApp
→ WhatsApp Business API (Z-API / Twilio) → webhook
→ FastAPI: validate + save contact/ticket to database
→ Pipeline (clean → normalize → vectorize)
→ ML Model: category + confidence score
→ Score ≥ 0.75?
    Yes → LLM attempts automatic resolution
            → Customer confirms resolution?
                Yes → close ticket as resolved
                No  → escalate to human queue
    No  → goes directly to human queue (low confidence flag)
→ Human queue ordered by dynamic priority (priority aging)
→ Agent responds via SmartTicket interface
→ System sends response via WhatsApp API
→ Everything stored in database → analytics + retraining
```

### Technical pipeline (reference — current code)

```text
Client
→ API (FastAPI)
→ Validation
→ classify_ticket → predict_category (pipeline: clean → normalize → vectorize)
→ triage_prediction (urgency + queue_target)
→ save_ticket_prediction → PostgreSQL (tickets)
→ JSON response (text echo + category + score + urgency + queue_target)
```

*(LLM step remains future — see `app/services/llm_service.py` stub.)*

---

## Offline flow (training)

```text
Dataset
→ Cleaning / pipeline
→ Feature engineering (TF-IDF + classifier)
→ Train model
→ Evaluate
→ Save model artifacts (paths TBD per environment; blob store if/when ADR says so)
```

---

## Folder responsibilities

- `app/api` — routes and HTTP handling
- `app/services` — `classify_ticket`, **`triage_prediction`** (`ticket_triage.py`), `run_pipeline`, `llm_service` stub
- `app/ml` — training and prediction
- `app/db` — SQLAlchemy models (`Ticket`), session factory (`DATABASE_URL`), repository writes
- `app/utils` — reusable text functions
- `app/data` — datasets (not production DB)
- `app/core` — configuration (`config.py`, **`triage_settings.py`**), limits; env keys in `api-contracts.md` / `.env.example`
- `db/migrations/` — hand-written SQL for PostgreSQL schema advances (e.g. add columns); not Alembic
- `scripts/` — thin CLI wrappers (e.g. pytest from repo root, `post_test_ticket.py`); must call logic in `app/`, not duplicate it

---

## Database structure

### Implemented (`tickets`)

| Column | Notes |
|--------|--------|
| `id` | UUID PK |
| `text_raw` | Request body `text` |
| `text_processed` | Output of preprocessing before vectorization |
| `category` | Predicted label |
| `score` | Model confidence |
| `urgency` | `HIGH` \| `MEDIUM` \| `LOW` — from **`triage_prediction`** / category map |
| `queue_target` | `human` \| `llm` — from score vs **`SMARTTICKET_LLM_MIN_SCORE`** |
| `status` | Default `classified` |
| `created_at` | Server default timestamp (timezone-aware) |

**Greenfield:** `Base.metadata.create_all` matches this model (see README).

**Existing PostgreSQL:** apply **`db/migrations/001_add_urgency_queue_target.sql`** if the table predates these columns. SQLite tests build schema from metadata only.

### Planned (product MVP — not implemented)

Align with longer-term vision:

- **CONTACTS** — whatsapp_number, name, is_customer, became_customer_at
- **TICKETS** (extended) — priority, priority_score, assigned_to, resolved_by (beyond current columns)
- **MESSAGES** — ticket_id, direction (inbound/outbound), sent_by (llm/human/system)
- **FEEDBACK** — ticket_id, correct_category, was_classification_correct, agent_id
- **CONVERSIONS** — contact_id, ticket_id, converted_at

---

## Tech stack

| Component | Technology |
|-----------|------------|
| Backend / API | Python + FastAPI |
| ML | Scikit-learn (TF-IDF + Logistic Regression) |
| Persistence | SQLAlchemy + PostgreSQL (`DATABASE_URL`) |
| LLM | OpenAI / LangChain deps installed; **`app/services/llm_service.py`** stub — not wired to routes |
| Database hosting | Supabase (MVP), Railway/RDS (production) *(examples)* |
| WhatsApp | Z-API (Brazil) or Twilio *(planned)* |
| Real-time | WebSockets via FastAPI — polling for demo |
| Agent interface | Streamlit (demo) → React / Next.js (production) |
| Scheduled jobs | APScheduler (priority aging + retraining) |
| Data processing | Pandas |
