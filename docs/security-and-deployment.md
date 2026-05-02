# Security and deployment (MVP)

Operational decisions and follow-ups. For request JSON shapes, see `api-contracts.md`.

## Done in code (MVP)

- **`DATABASE_URL`:** SQLAlchemy reads this env var at runtime (`app/db/session.py`). Local/dev uses **`.env`** (loaded by `python-dotenv` in `app.main`). **Never commit** secrets — see repo **`.env.example`** for variable names only.

- **`POST /predict` persistence:** successful responses require a working DB session (configured URL + reachable server + schema). Missing URL → **503** `Database persistence not configured.` Failed transaction → **503** `Could not persist ticket; database unavailable.` Prefer **TLS** (`sslmode=require` in URL or proxy) for hosted Postgres.

- **`POST /predict` body size:** `text` is limited to `MAX_TICKET_TEXT_CHARS` in `app/core/limits.py`, enforced by `PredictRequest` in `app/api/schemas.py`. Requests over the limit return **422** (validation error).

- **Offline training:** `train_model` in `app/ml/train.py` drops CSV rows whose raw text column exceeds the same `MAX_TICKET_TEXT_CHARS`, keeping the training distribution aligned with what the API accepts.

## Documented for now (review before public or production)

### Model files (`joblib` / pickle)

Inference loads `model.pkl` and `vectorizer.pkl` with `joblib.load()`. Unpickling can execute code if a file is replaced by a malicious actor who can **write** to the artifact path.

**Mitigation:** keep artifacts on trusted storage, restrict filesystem permissions, deploy only from trusted builds. Prefer integrity checks (hash/signature) on the deployment pipeline if the threat model requires it. Replacing pickle with a safer on-disk format is a larger refactor; track explicitly if needed.

### Authentication and rate limiting

The MVP API has **no** API key or OAuth on **`POST /predict`**, **`GET /tickets`**, or **`GET /health`** by design until you need it. If the service is exposed to the public internet, add at least one of: **network restriction**, **API gateway rate limits**, or **application-level auth**.

### Error responses in production

Run the ASGI server with **debug/reload off** in production so stack traces and internals are not returned to clients. Unhandled 500s should be logged on the server; the client can see a generic message depending on your FastAPI settings.

**Example (adjust host/port as needed):**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Do **not** use `--reload` in production. If you use `workers`, configure them in your process manager (e.g. gunicorn + uvicorn workers) per your hosting docs.

### CORS

CORS is not enabled in `app/main.py` by default. When a browser front end calls the API, configure `CORSMiddleware` with **explicit** allowed origins; avoid `allow_origins=["*"]` with credentialed requests.

### OpenAPI / docs

FastAPI exposes `/docs` and `/redoc`. For a public API you may **disable** or **protect** them (reverse proxy, env flag, or mounting conditionally) so internal schemas are not trivially browsable.

### Privacy (PII)

`POST /predict` returns the same `text` in the response for traceability. Logging proxies or APM tools may then store customer content twice; align retention and redaction with your policy.

**`GET /tickets`** returns **full** `text_raw` and `text_processed` for each row (same sensitivity as accepting them on `POST /predict`). The MVP ships **without** application-level auth: restrict access via **private network**, **API gateway**, or **TLS + credentials** aligned with your threat model before exposing the queue read API broadly.

### Streamlit Community Cloud (`demo/streamlit_app.py`)

The demo calls the FastAPI app **from Streamlit’s Python runtime** (server-side `requests`), so **CORS is not required** for this UI path. Configure the deployed API URL as **`SMARTTICKET_API_BASE_URL`** via **Streamlit app secrets** (dashboard) or local **`.streamlit/secrets.toml`** from **`secrets.toml.example`** — do **not** commit real URLs or tokens. The API host must be **reachable from the public internet** (Streamlit Cloud cannot use `127.0.0.1` on your machine). Prefer **HTTPS** for the API in line with the rest of this doc.

## Single source of truth

| Topic | Where |
|--------|--------|
| Max `text` length (HTTP + training row filter) | `app/core/limits.py` → `MAX_TICKET_TEXT_CHARS` |
| Database URL (never commit real credentials) | Env **`DATABASE_URL`** · template **`/.env.example`** |
| LLM vs human routing threshold | **`SMARTTICKET_LLM_MIN_SCORE`** · `app/core/triage_settings.py` |


Tuning the limit: change the constant, run tests, and update `api-contracts.md` if the documented number is mentioned explicitly.
