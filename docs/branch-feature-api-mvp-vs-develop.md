# `feature/api-mvp` vs `develop`

This page summarizes what the branch **`feature/api-mvp`** adds on top of **`develop`**, to help code review and merge planning. It was last updated when aligning docs with that delta.

**Authorship:** The MVP code and documentation described here (including the FastAPI layer) is **Lucas only** — not Salim or other teammates; see `docs/team-responsibilities.md` (note at top) and `docs/project-context.md` (ownership section).

## Summary

| Area | `develop` | `feature/api-mvp` |
|------|-----------|-------------------|
| **HTTP API** | `app/main.py` mounts a router, but `app/api/routes.py` is a **stub** (TODOs only). | **`GET /health`** and **`POST /predict`** are implemented; handlers call `predict_category`. |
| **Schemas** | `app/api/schemas.py` is almost empty (module docstring only). | **`PredictRequest`**, **`PredictResponse`**, **`HealthResponse`** with Pydantic; `text` has **`max_length`** from `app.core.limits`. |
| **Limits** | No shared constant file. | **`app/core/limits.py`**: `MAX_TICKET_TEXT_CHARS` (50_000) drives API validation and training row filtering. |
| **Training** | No `dropna`; no max-length filter on raw CSV text before the pipeline. | **Drops** rows with missing text/label; **drops** rows where raw `texts` string length `> MAX_TICKET_TEXT_CHARS` (aligned with `POST /predict`). |
| **Config** | Paths from repo root defaults. | Same defaults plus **optional env overrides**: `SMARTTICKET_MODEL_PATH`, `SMARTTICKET_VECTORIZER_PATH`, `SMARTTICKET_DATASET_PATH`. |
| **Errors** | N/A (no routes). | **`POST /predict`**: **422** if body invalid or `text` too long; **503** if `predict_category` hits missing artifacts (message points to `GET /health`). **`GET /health`**: **200** `ready` or **503** `not_ready` (minimal JSON, no path leakage). |
| **Docs: contracts** | Short `api-contracts.md` (mainly `POST /predict` example). | **Expanded** `docs/api-contracts.md`: technical MVP table, `GET /health`, status codes, env vars, appendix for future product routes. |
| **Security / ops** | — | New **`docs/security-and-deployment.md`**: text length, pickle trust, no auth in MVP, production `uvicorn` notes, CORS/OpenAPI, PII in responses. |
| **Tests** | `tests/test_api.py` not exercising real routes (or missing). | **`TestClient` tests** for `/health` shape, `/predict` success (mocked ML), 422, over-max-length, 503 on missing artifacts. |
| **Dependencies** | (baseline `requirements.txt`) | **Removed unused `black`** from requirements in this workstream. |

## What is still *not* in this branch (vs full product MVP)

Merging `feature/api-mvp` into `develop` **does not** complete the end-to-end product MVP. Still outstanding, among other things:

- **Database persistence** after prediction (tickets, contacts, messages) and schemas tied to the DB.
- **Authentication, rate limiting, CORS** for a public or browser-facing API (see `docs/security-and-deployment.md` — noted as follow-ups).
- **WhatsApp / webhooks**, **agent UI**, **LLM** flows, **priority queue** as in `docs/product-vision-*.md`.
- **Operational retrain script** (e.g. `scripts/retrain.py`) and automated feedback-driven retraining.
- **Hardening** of `/docs` and `/redoc` if the API is exposed untrusted.

## After merge

When `feature/api-mvp` is merged into `develop`:

- Update this document’s “Summary” if needed, or replace with a short line: *“Content absorbed into `develop`; see `api-contracts.md` and `project-context.md` for current status.”*
- Re-check **`docs/project-context.md`** “Development order” and **`README.md`** “Features / Roadmap” so they match the default branch.
