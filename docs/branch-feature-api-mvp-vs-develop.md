# `feature/api-mvp` vs `develop`

Summarizes what **`feature/api-mvp`** introduced relative to an older **`develop`** baseline (stub routes), plus **follow-on persistence work** that may land on **`feature/database`** or merged branches — use git history for the exact delta after merges.

**Authorship:** MVP FastAPI + persistence wiring described here is **Lucas** — see `docs/team-responsibilities.md` and `docs/project-context.md`.

## Summary

| Area | Older `develop` | Current MVP stack (`feature/api-mvp` + persistence) |
|------|-----------------|------------------------------------------------------|
| **HTTP API** | `app/api/routes.py` stub (TODOs). | **`GET /health`**, **`POST /predict`**; handlers call **`classify_ticket`** → `predict_category`. |
| **Schemas** | Near-empty `schemas.py`. | **`PredictRequest`**, **`PredictResponse`**, **`HealthResponse`**; `max_length` from **`app/core/limits.py`**. |
| **Limits** | No shared constant. | **`MAX_TICKET_TEXT_CHARS`** — API validation + **`train_model`** row filter. |
| **Config** | Root-relative defaults only. | **`SMARTTICKET_*`** env overrides for model / vectorizer / dataset paths (`app/core/config.py`). |
| **Persistence** | None. | **`DATABASE_URL`** → SQLAlchemy; **`tickets`** table (`app/db/models.py`); **`save_ticket_prediction`**; **`POST /predict`** returns **503** if DB unavailable/unconfigured or write fails. |
| **Services** | Direct ML imports from routes (historically). | **`app/services/classifier.py`** — `ClassificationResult` + **`classify_ticket`**. |
| **Dependencies** | Baseline `requirements.txt`. | **`sqlalchemy`**, **`psycopg2-binary`**; **`openai`**, **`langchain`** present — **`app/services/llm_service.py`** is a stub only. |
| **Tests** | No/little route coverage. | **`tests/test_api.py`** (`TestClient`, mocked classifier); **`tests/test_persistence.py`** (repository + DB overrides + rollback); **`conftest.py`** clears **`DATABASE_URL`** during pytest. |
| **Docs** | Minimal contracts. | **`docs/api-contracts.md`**, **`docs/security-and-deployment.md`**, this file; **`README`** setup includes DB + **`.env.example`**. |

## Still *not* in scope (vs full product MVP)

- **Contacts**, **messages**, urgency columns, **GET/list ticket** APIs, auth, rate limits, webhooks/WhatsApp, agent UI, **LLM** in response path, **RabbitMQ** / priority workers, **Alembic** migrations.

## After merges

When deltas are absorbed into **`develop`**, shorten this file to a pointer (`README`, `project-context`, `architecture.md`) or refresh the table against **`git diff develop...HEAD`**.
