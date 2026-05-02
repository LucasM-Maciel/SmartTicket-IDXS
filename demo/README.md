# SmartTicket Streamlit demo

Browser UI that calls your **deployed** FastAPI backend (`POST /predict`, `GET /tickets`). Queue ordering is entirely determined by the API.

## Local run

```bash
# Terminal 1 — API (Postgres + model artifacts required for full flow)
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2
streamlit run demo/streamlit_app.py
```

Optional: point to a remote API only:

```bash
set SMARTTICKET_API_BASE_URL=https://your-api.example.com
streamlit run demo/streamlit_app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub.
3. **New app** → pick the repo and branch.
4. **Main file:** `demo/streamlit_app.py`
5. **Advanced settings** → **Requirements file:** `demo/requirements.txt`  
   (Use this path so the cloud build does not install the full ML stack from the repo root `requirements.txt`.)
6. **App secrets** (required — the cloud cannot reach `127.0.0.1`):

   ```toml
   SMARTTICKET_API_BASE_URL = "https://your-fastapi-service.example.com"
   ```

   No trailing slash. Use the public **HTTPS** URL of your API (e.g. Railway, Render, Fly.io).

7. Deploy your **FastAPI app separately** with:
   - `DATABASE_URL`
   - Model artifacts on disk or your image
   - Optional demo threshold: `SMARTTICKET_LLM_MIN_SCORE=0.30` so more tickets route to the LLM queue

The Streamlit app runs **server-side** `requests` to your API, so you do not need CORS on FastAPI for this UI.

### Local secrets (optional)

Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` (that file is gitignored) and set `SMARTTICKET_API_BASE_URL` if you want to override localhost without using the sidebar.
