# API contracts (SmartTicket-IDXS)

> **Branch note:** For what is implemented on `feature/api-mvp` vs the current `develop` baseline, see **`branch-feature-api-mvp-vs-develop.md`**.

> This file describes **HTTP JSON** contracts. The **primary scope** below is the **technical MVP** (synthetic tickets → API → ML → persist/queue *as a design target*). Broader product routes (WhatsApp, attendant CRUD) live in the appendix.

---

## Technical MVP (scope)

Matches the **“Technical SmartTicket MVP”** diagram: a **modular FastAPI** orchestrates a **test/synthetic** ticket string, a **pre-processing + prediction** path, then **persistence, urgency, and priority** as product logic.

| Diagram box | In the technical MVP (typical) |
|-------------|----------------------------------|
| **Test dataset** (“Synthetic tickets”) | Not a separate *route*: a **client** (script, `curl`, `httpx`, tests) sends `{"text": "…"}` to the API. Same idea as “synthetic tickets in”. |
| **API SmartTicket (modular)** | `FastAPI` + `app/api/routes.py` (+ future services). |
| **Pre-processing pipeline** + **Prediction model** | `run_pipeline` + `predict_category` inside `POST /predict` (and `GET /health` for artifact *files* only). |
| **DB** (“Persist ticket + classification + score”) | **Planned in code** as DB layer — **not** part of the minimal HTTP surface until you add persistence. |
| **Priority queue** (urgency / “prioritized by …”) | **Planned** as **logical** queue (e.g. Postgres + scheduler), **not** a separate public REST resource in the first technical slice. |

**HTTP surface for the technical MVP (keep small):**

| Path | Role |
|------|------|
| `GET /health` | Readiness: artifact *files* exist (paths from `app/core/config.py`, overridable via env — see *Conventions*). |
| `POST /predict` | One-shot classification on a `text` string; returns `text` echo + `category` + `score`. |

Optional later without changing the diagram’s core story: `GET /version` (debug only).

**Status codes you care about first:** **200** on success, **422** on invalid body (including `text` over the max length), **503** when not ready to infer (missing artifacts) — see each route below.

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

**Purpose:** Run the ML pipeline and classifier on a **single** string — the stand-in for a **synthetic** ticket line from the diagram. **No** DB write in the baseline contract (persistence is a follow-up feature).

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
  "category": "cancellation",
  "score": 0.92
}
```

### Notes

- After preprocessing, if the text is empty or only whitespace, the implementation returns `category: "unknown"`, `score: 0.0` without loading model artifacts (this covers `{"text": ""}` and bodies like `{"text": "   "}`).
- If model artifacts are missing when inference runs, the API responds with **503** and FastAPI’s default error body, with `detail` exactly:

  `Model artifacts missing; check GET /health`

  (consistent with `GET /health` returning `not_ready` when files are absent.)

---

## Conventions (technical MVP)

- **Content-Type** for request bodies: `application/json` unless noted.
- **Errors:** FastAPI default `{"detail": ...}` is fine until you add a shared error schema. For `POST /predict` artifact failures, `detail` is stable (see route notes above).
- **Limits:** `app/core/limits.py` — `MAX_TICKET_TEXT_CHARS` caps `text` on `POST /predict` (Pydantic) and excludes over-long rows in `train_model` so training matches the API bound.
- **Paths (`app/core/config.py`):** defaults point at the repo layout (`artifacts/*.pkl`, dataset under `app/data/...`). Optional overrides — if set to a non-empty string, that path is used (`~` is expanded):

  | Variable | Role |
  |----------|------|
  | `SMARTTICKET_MODEL_PATH` | Trained model `.pkl` |
  | `SMARTTICKET_VECTORIZER_PATH` | Vectorizer `.pkl` |
  | `SMARTTICKET_DATASET_PATH` | Training CSV (training script / notebooks) |

---

## Appendix — product MVP (later)

The following are **not** required to validate the **technical** diagram end-to-end in code. Add them when the **DB + channel + UI** slices start.

| Area | Path(s) (illustrative) | Notes |
|------|------------------------|--------|
| Inbound WhatsApp / BSP | `POST /webhooks/{provider}` (TBD) | Body depends on Z-API, Twilio, Meta, etc. |
| Tickets (attendant) | `GET/POST /tickets`, `GET/PATCH /tickets/{id}` | Needs PostgreSQL and auth decisions |
| Outbound to WhatsApp | Outbound **HTTP from backend** to provider | Usually **not** a public route on your API |

**Optional:** `GET /version` — return `{ "name": "…", "version": "…" }` aligned with `app/main.py`.

**Further fields:** LLM suggest/resolve flows, WebSocket payloads, admin auth — document in a addendum when Sprint/product rules are locked (see `docs/reuniao-regras-negocio.md`).

**Product-tier examples** (tickets list/detail, webhook shape) were folded into this appendix; when you need full request/response examples, expand subsections here or add `docs/api-contracts-product.md`.
