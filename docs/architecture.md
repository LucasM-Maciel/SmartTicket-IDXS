# System Architecture

> Last updated: 2026-04-16

## Overview

The system follows a layered architecture:

- **API layer** — HTTP requests, validation, persistence orchestration
- **Service layer** — pipeline orchestration (`run_pipeline`)
- **ML layer** — training (`train_model`) and inference (`predict_category`)
- **Utils layer** — text cleaning and normalization
- **Data layer** — datasets, relational DB (tenancy pattern TBD), model artifacts

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

### Technical pipeline (reference)

```text
User / channel
→ API (FastAPI)
→ Validation
→ Pipeline (clean → normalize → vectorize in inference)
→ ML model (category + score)
→ (Future) LLM response
→ Save to database
→ Return response
```

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
- `app/services` — pipeline and future non-ML services
- `app/ml` — training and prediction
- `app/utils` — reusable text functions
- `app/data` — datasets (not production DB)
- `app/core` — configuration (paths, columns); app-wide settings may split to `settings` for env-based deployment config
- `scripts/` — thin CLI wrappers (e.g. pytest from repo root); must call logic in `app/`, not duplicate it

---

## Database structure (planned)

- **CONTACTS** — whatsapp_number, name, is_customer, became_customer_at
- **TICKETS** — text, text_processed, category, score, priority, priority_score, status, assigned_to, resolved_by
- **MESSAGES** — ticket_id, direction (inbound/outbound), sent_by (llm/human/system)
- **FEEDBACK** — ticket_id, correct_category, was_classification_correct, agent_id
- **CONVERSIONS** — contact_id, ticket_id, converted_at

---

## Tech stack

| Component | Technology |
|-----------|------------|
| Backend / API | Python + FastAPI |
| ML | Scikit-learn (TF-IDF + Logistic Regression) |
| LLM | OpenAI API *(planned)* |
| Database | PostgreSQL — Supabase (MVP), Railway/RDS (production) |
| WhatsApp | Z-API (Brazil) or Twilio *(planned)* |
| Real-time | WebSockets via FastAPI — polling for demo |
| Agent interface | Streamlit (demo) → React / Next.js (production) |
| Scheduled jobs | APScheduler (priority aging + retraining) |
| Data processing | Pandas |
