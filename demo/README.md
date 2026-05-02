# SmartTicket Streamlit demo

Calls **`POST /predict`** and **`GET /tickets`**; ordering follows the API only.

## Local run

```bash
# Terminal 1 — API (Postgres + model artifacts for full flow)
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2
streamlit run demo/streamlit_app.py
```

Optional remote API:

```bash
set SMARTTICKET_API_BASE_URL=https://your-api.example.com
streamlit run demo/streamlit_app.py
```

## Streamlit Community Cloud

1. Repo on GitHub → [share.streamlit.io](https://share.streamlit.io/) → **New app**.
2. **Main file:** `demo/streamlit_app.py`
3. **Advanced → Requirements file:** `demo/requirements.txt` (avoids installing the repo-root ML stack).
4. **Secrets** (required — Cloud cannot reach your laptop):

   ```toml
   SMARTTICKET_API_BASE_URL = "https://your-fastapi-service.example.com"
   ```

   HTTPS, no trailing slash. With this secret set, the sidebar URL field is **locked** (SSRF-safe for a public app).

5. Run FastAPI elsewhere with `DATABASE_URL`, artifacts, and optional **`SMARTTICKET_LLM_MIN_SCORE`** (e.g. `0.30` to fill the LLM queue in demos).

Server-side `requests` → **no CORS** needed on FastAPI for this UI.

### Troubleshooting

- **Error about localhost on Cloud:** set `SMARTTICKET_API_BASE_URL` to your **public** `https://` API URL.
- **Empty queues / errors:** API up, `GET /health` → `ready`, Postgres reachable from the API.

### Local fixed URL (optional)

Copy `.streamlit/secrets.toml.example` → `.streamlit/secrets.toml` (gitignored) to pin the API URL without using the sidebar — same lock behavior as Cloud.
