# `feature/api-mvp` vs `develop`

Summarizes what **`feature/api-mvp`** introduced relative to an older **`develop`** baseline (stub routes), plus **follow-on persistence work** that may land on **`feature/database`** or merged branches — use git history for the exact delta after merges.

**Authorship:** MVP FastAPI + persistence wiring described here is **Lucas** — see `docs/team-responsibilities.md` and `docs/project-context.md`.

## Summary

| Area | Older `develop` | Current MVP stack (`feature/api-mvp` + persistence) |
|------|-----------------|------------------------------------------------------|
| **HTTP API** | `app/api/routes.py` stub (TODOs). | **`GET /health`**, **`POST /predict`**; **`classify_ticket`** → **`triage_prediction`** → persist **`urgency`** + **`queue_target`**. |
| **Schemas** | Near-empty `schemas.py`. | **`PredictRequest`**, **`PredictResponse`** (+ **`urgency`**, **`queue_target`**), **`HealthResponse`**; `max_length` from **`app/core/limits.py`**. |
| **Limits** | No shared constant. | **`MAX_TICKET_TEXT_CHARS`** — API validation + **`train_model`** row filter. |
| **Config** | Root-relative defaults only. | **`SMARTTICKET_*`** paths (`app/core/config.py`); **`SMARTTICKET_LLM_MIN_SCORE`** (`app/core/triage_settings.py`). |
| **Persistence** | None. | **`DATABASE_URL`** → SQLAlchemy; **`tickets`** incl. **`urgency`**, **`queue_target`**; **`db/migrations/001_add_urgency_queue_target.sql`** for legacy Postgres. |
| **Services** | Direct ML imports from routes (historically). | **`classifier.py`**, **`ticket_triage.py`**. |
| **Dependencies** | Baseline `requirements.txt`. | **`sqlalchemy`**, **`psycopg2-binary`**. LLM deps **commented** until `llm_service` is implemented. |
| **Tests** | No/little route coverage. | **`test_api`**, **`test_persistence`**, **`test_ticket_triage`**, **`test_triage_settings`**; **`conftest.py`** clears **`DATABASE_URL`**. |
| **Docs** | Minimal contracts. | **`docs/api-contracts.md`**, **`docs/security-and-deployment.md`**, this file; **`README`** setup includes DB + **`.env.example`**. |

## Still *not* in scope (vs full product MVP)

- **Contacts** / **messages** beyond current `tickets` columns, **GET/list ticket** APIs, auth, rate limits, webhooks/WhatsApp, agent UI, **LLM** in the customer-facing response path, **RabbitMQ** / priority workers, **Alembic** migrations.

## After merges

When deltas are absorbed into **`develop`**, shorten this file to a pointer (`README`, `project-context`, `architecture.md`) or refresh the table against **`git diff develop...HEAD`**.
