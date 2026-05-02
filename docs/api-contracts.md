# API contracts (SmartTicket-IDXS)

> **Branch note:** Stack includes **`DATABASE_URL`** persistence, **`urgency`**, **`queue_target`**, and **`SMARTTICKET_LLM_MIN_SCORE`** — see **`branch-feature-api-mvp-vs-develop.md`** + `git diff`.

> This file describes **HTTP JSON** contracts. The **primary scope** below is the **technical MVP** (synthetic tickets → API → ML → persist/queue *as a design target*). Broader product routes (WhatsApp, attendant CRUD) live in the appendix.

---

## Technical MVP (scope)

Matches the **“Technical SmartTicket MVP”** diagram: a **modular FastAPI** orchestrates a **test/synthetic** ticket string, a **pre-processing + prediction** path, then **persistence, urgency, and priority** as product logic.

| Diagram box | In the technical MVP (typical) |
|-------------|----------------------------------|
| **Test dataset** (“Synthetic tickets”) | Not a separate *route*: a **client** (script, `curl`, `httpx`, tests) sends `{"text": "…"}` to the API. Same idea as “synthetic tickets in”. |
| **API SmartTicket (modular)** | `FastAPI` + `app/api/routes.py` (+ future services). |
| **Pre-processing pipeline** + **Prediction model** | `run_pipeline` inside **`classify_ticket`** → `predict_category`; **`GET /health`** probes artifact *files* only. |
| **DB** (“Persist ticket + classification + score + routing”) | **Implemented:** includes **`urgency`** and **`queue_target`**; see `ticket_triage.py` / `triage_settings.py`. |
| **Priority queue** (broker / workers) | **Not** implemented; **`queue_target`** is a persisted **routing flag** only (`human` / `llm`). |

**HTTP surface for the technical MVP (keep small):**

| Path | Role |
|------|------|
| `GET /health` | Readiness: artifact *files* exist (paths from `app/core/config.py`, overridable via env — see *Conventions*). |
| `POST /predict` | One-shot classification on a `text` string; returns `text` echo + `category` + `score` + `urgency` + `queue_target`. |
| `GET /tickets` | Paginated queue read: tickets ordered by **urgency** tier (HIGH → MEDIUM → LOW), then **FIFO** by `created_at`; optional `queue_target` filter (`human` / `llm`). |

Optional later without changing the diagram’s core story: `GET /version` (debug only).

**Status codes you care about first:** **200** on success; **422** on invalid body or query (e.g. `text` over max length, invalid `queue_target`); **503** when not ready to infer (missing artifacts), when the database is not configured, or when a DB read/write fails — see each route below.

---

## `GET /health` (technical MVP)

**Purpose:** Readiness — check that model artifact **files** exist on disk (`model.pkl`, `vectorizer.pkl` via `app/core/config.py`). Does **not** load pickles.

### Response (JSON)

| HTTP | `status` | When |
|------|----------|------|
| 200 | `ready` | Both files present |
| 503 | `not_ready` | One or both missing (probes that use HTTP status see failure) |

```json
{
  "status": "ready"
}
```

### Notes

- The body is intentionally **minimal** (`status` only) so a public probe does not reveal *which* artifact is missing.
- Returning **200** with `not_ready` in the body **without** **503** is a weaker contract; if you do that, say so here and in the route.

---

## `POST /predict` (technical MVP)

**Purpose:** Run the ML pipeline and classifier on a **single** string — the stand-in for a **synthetic** ticket line from the diagram. After a successful prediction, the API **persists** raw text, processed text, category, score, **urgency** (`HIGH` / `MEDIUM` / `LOW`), and **queue_target** (`human` / `llm`) when `DATABASE_URL` is configured (otherwise **503**). Rules live in `app/services/ticket_triage.py` and `app/core/triage_settings.py`.

### Request

```json
{
  "text": "I want to cancel my order"
}
```

- `text` is required and must be a JSON string (including `""`). The schema does not reject empty or whitespace-only values; those still go through preprocessing.
- **Max length:** `text` may not exceed **`MAX_TICKET_TEXT_CHARS`** (see `app/core/limits.py`, currently **50_000** characters). If it does, the API responds with **422** (validation error).

### Response (200)

```json
{
  "text": "I want to cancel my order",
  "category": "cancellation_request",
  "score": 0.92,
  "urgency": "HIGH",
  "queue_target": "llm"
}
```

- `urgency` is derived from the predicted **category** (see `docs/project-context.md`).
- `queue_target` uses the classification **score** vs `SMARTTICKET_LLM_MIN_SCORE` (default **0.75**): scores **≥** threshold → `llm`, otherwise `human`.

### Notes

- After preprocessing, if the text is empty or only whitespace, the implementation returns `category: "unknown"`, `score: 0.0` without loading model artifacts (this covers `{"text": ""}` and bodies like `{"text": "   "}`).
- If model artifacts are missing when inference runs, the API responds with **503** with `detail` exactly: `Model artifacts missing; check GET /health` (consistent with `GET /health` returning `not_ready` when files are absent).
- If `DATABASE_URL` is unset, **503** with `detail`: `Database persistence not configured.`
- If the DB transaction fails, **503** with `detail`: `Could not persist ticket; database unavailable.`

---

## `GET /tickets` (technical MVP)

**Purpose:** Read persisted tickets in **service queue order**: urgency tier first (**HIGH**, then **MEDIUM**, then **LOW**), then oldest **`created_at`** first within the same tier. Uses read-only SQL (`app/db/queue_repository.py`).

### Query parameters

| Parameter | Default | Notes |
|-----------|---------|------|
| `queue_target` | *(omit)* | If `human` or `llm`, only tickets with that routing flag. |
| `limit` | `50` | Page size, **1–100**. |
| `offset` | `0` | Rows to skip (pagination). |

### Response (200)

JSON object with **`items`** (array of ticket rows), **`total`** (matching rows for the filter, before pagination), **`limit`**, **`offset`**.

Each item includes: `id`, `text_raw`, `text_processed`, `category`, `score`, `urgency`, `queue_target`, `status`, `created_at`.

### Errors

- **`DATABASE_URL` unset:** **503** — `Database persistence not configured.`
- **DB query failure:** **503** — `Could not load tickets; database unavailable.`
- **Invalid `queue_target`** (not `human` / `llm`): **422** validation error.

---

## Conventions (technical MVP)

- **Content-Type** for request bodies: `application/json` unless noted.
- **Errors:** FastAPI default `{"detail": ...}` is fine until you add a shared error schema. For `POST /predict` artifact failures, `detail` is stable (see route notes above).
- **Limits:** `app/core/limits.py` — `MAX_TICKET_TEXT_CHARS` caps `text` on `POST /predict` (Pydantic) and excludes over-long rows in `train_model` so training matches the API bound.
- **Startup (normalization parity):** FastAPI **`lifespan`** in **`app/main.py`** calls **`ensure_nltk_stopwords()`** (`app/core/nltk_bootstrap.py`) — may download NLTK **stopwords** on first run; if download is impossible, the process still starts (`normalize_text` may **passthrough**). See **`docs/security-and-deployment.md`** (egress / air-gapped).
- **Paths (`app/core/config.py`):** defaults point at the repo layout (`artifacts/*.pkl`, dataset under `app/data/...`). Optional overrides — if set to a non-empty string, that path is used (`~` is expanded):

  | Variable | Role |
  |----------|------|
  | `DATABASE_URL` | PostgreSQL URL for SQLAlchemy (**required** at runtime for **`POST /predict`** and **`GET /tickets`**; see `.env.example`) |
  | `SMARTTICKET_LLM_MIN_SCORE` | Score threshold in **[0, 1]** (clamped); `score >=` value → `queue_target: "llm"`, else `"human"` — default **0.75** if unset/invalid (`app/core/triage_settings.py`) |
  | `SMARTTICKET_MODEL_PATH` | Trained model `.pkl` |
  | `SMARTTICKET_VECTORIZER_PATH` | Vectorizer `.pkl` |
  | `SMARTTICKET_DATASET_PATH` | Training CSV (training script / notebooks) |
  | `SMARTTICKET_DISABLE_OPENAPI` | If **`1`** / **`true`** / **`yes`**, hides **`/docs`**, **`/redoc`**, and the OpenAPI schema URL (`app.core.config.fastapi_documentation_kwargs` → **`app/main.py`**) |

---

## Appendix — product MVP (later)

The following are **not** required to validate the **technical** diagram end-to-end in code. Add them when the **DB + channel + UI** slices start.

| Area | Path(s) (illustrative) | Notes |
|------|------------------------|--------|
| Inbound WhatsApp / BSP | `POST /webhooks/{provider}` (TBD) | Body depends on Z-API, Twilio, Meta, etc. |
| Tickets (attendant) | `GET /tickets` ✅ MVP queue read · `GET/PATCH /tickets/{id}` | List/detail/patch for agents; **auth** still product backlog |
| Outbound to WhatsApp | Outbound **HTTP from backend** to provider | Usually **not** a public route on your API |

**Optional:** `GET /version` — return `{ "name": "…", "version": "…" }` aligned with `app/main.py`.

**Further fields:** LLM suggest/resolve flows, WebSocket payloads, admin auth — document in a addendum when Sprint/product rules are locked (see `docs/reuniao-regras-negocio.md`).

**Product-tier examples** (tickets list/detail, webhook shape) were folded into this appendix; when you need full request/response examples, expand subsections here or add `docs/api-contracts-product.md`.
