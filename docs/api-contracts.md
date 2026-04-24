# API contracts (SmartTicket-IDXS)

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
| `GET /health` | Readiness: artifact *files* exist (`.pkl` paths from `app/core/config.py`). |
| `POST /predict` | One-shot classification on a `text` string; returns `text` echo + `category` + `score`. |

Optional later without changing the diagram’s core story: `GET /version` (debug only).

**Status codes you care about first:** **200** on success, **422** on invalid body, **503** when not ready to infer (missing artifacts) — see each route below.

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
  "status": "ready",
  "model_present": true,
  "vectorizer_present": true
}
```

### Notes

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

- `text` is required, string.

### Response (200)

```json
{
  "text": "I want to cancel my order",
  "category": "cancellation",
  "score": 0.92
}
```

### Notes

- If preprocessing yields only whitespace, the implementation may return `category: "unknown"`, `score: 0.0` without loading model artifacts.
- If artifacts are missing on first load, a **503** (or `detail` error) is appropriate; keep behavior aligned with `GET /health`.

---

## Conventions (technical MVP)

- **Content-Type** for request bodies: `application/json` unless noted.
- **Errors:** FastAPI default `{"detail": ...}` is fine until you add a shared error schema.

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
