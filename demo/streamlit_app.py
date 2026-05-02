"""Streamlit demo: calls ``POST /predict`` and ``GET /tickets`` (queue order = API).

Run locally: ``streamlit run demo/streamlit_app.py``. Deploy and env vars: ``demo/README.md``.
"""

from __future__ import annotations

import json
import os
from typing import Any
from urllib.parse import urljoin

import requests
import streamlit as st

DEFAULT_API_BASE = "http://127.0.0.1:8000"
REQUEST_TIMEOUT_S = 30


def _running_on_streamlit_cloud() -> bool:
    """Heuristic: Streamlit Community Cloud clones the repo under ``/mount/src`` (Linux)."""
    base = (os.environ.get("STREAMLIT_SERVER_BASE_URL") or "").strip().lower()
    if base.endswith(".streamlit.app"):
        return True
    if os.path.isdir("/mount/src"):
        return True
    return False


def _secret_api_base() -> str | None:
    """``SMARTTICKET_API_BASE_URL`` from ``st.secrets``, if set."""
    try:
        secrets = getattr(st, "secrets", None)
        if secrets is None or "SMARTTICKET_API_BASE_URL" not in secrets:
            return None
        url = str(secrets["SMARTTICKET_API_BASE_URL"]).strip().rstrip("/")
        return url or None
    except (FileNotFoundError, KeyError, TypeError, RuntimeError):
        return None


def _locked_api_base() -> str | None:
    """Secrets URL first; on Cloud only, fall back to env (locks sidebar when fixed)."""
    fixed = _secret_api_base()
    if fixed:
        return fixed
    if _running_on_streamlit_cloud():
        env_url = (os.environ.get("SMARTTICKET_API_BASE_URL") or "").strip().rstrip("/")
        if env_url:
            return env_url
    return None


def _is_non_public_api_host(url: str) -> bool:
    """True if the backend is clearly unreachable from Streamlit Cloud."""
    u = (url or "").strip().lower().rstrip("/")
    if not u:
        return True
    if u.startswith("http://127.") or u.startswith("http://localhost"):
        return True
    if u.startswith("http://0.0.0.0") or u.startswith("http://[::1]"):
        return True
    return False


def initial_api_base() -> str:
    """Local / unlocked: env, then secrets, then localhost."""
    env = (os.environ.get("SMARTTICKET_API_BASE_URL") or "").strip().rstrip("/")
    if env:
        return env
    u = _secret_api_base()
    if u:
        return u
    return DEFAULT_API_BASE


def _full_url(base: str, path: str) -> str:
    return urljoin(base.rstrip("/") + "/", path.lstrip("/"))


def _looks_like_railway_dashboard_url(url: str) -> bool:
    """``railway.com/project/...`` is the dashboard, not the deployed API."""
    return "railway.com/project" in (url or "").lower()


def _compact_api_error(status_code: int, body: Any) -> str:
    """Avoid dumping multi‑KB HTML (404 pages) into the UI."""
    if isinstance(body, dict) and "raw" in body:
        raw = body["raw"]
        if isinstance(raw, str):
            head = raw[:800].lower()
            if "<!doctype" in head or "<html" in head:
                return (
                    f"HTTP {status_code}: got HTML instead of JSON — wrong base URL or path. "
                    "Use your **deployed FastAPI hostname** (e.g. `https://<name>.up.railway.app`), "
                    "**not** the Railway **project** page (`railway.com/project/...`). "
                    "Check `https://…/health` in the browser."
                )
            if len(raw) > 400:
                return f"HTTP {status_code}: non-JSON response ({len(raw)} chars). Snippet: {raw[:180]}…"
    s = str(body)
    return s if len(s) <= 700 else s[:700] + "…"


def _get_json(base: str, path: str, params: dict[str, Any] | None = None) -> tuple[int, Any]:
    r = requests.get(_full_url(base, path), params=params or {}, timeout=REQUEST_TIMEOUT_S)
    try:
        body = r.json()
    except json.JSONDecodeError:
        body = {"raw": r.text}
    return r.status_code, body


def _post_json(base: str, path: str, payload: dict[str, Any]) -> tuple[int, Any]:
    r = requests.post(
        _full_url(base, path),
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=REQUEST_TIMEOUT_S,
    )
    try:
        body = r.json()
    except json.JSONDecodeError:
        body = {"raw": r.text}
    return r.status_code, body


def fetch_health(base: str) -> tuple[int, Any]:
    return _get_json(base, "/health")


def fetch_queue(base: str, queue_target: str | None, limit: int = 100) -> tuple[int, Any]:
    params: dict[str, Any] = {"limit": limit, "offset": 0}
    if queue_target is not None:
        params["queue_target"] = queue_target
    return _get_json(base, "/tickets", params=params)


def submit_predict(base: str, text: str) -> tuple[int, Any]:
    return _post_json(base, "/predict", {"text": text})


def _ticket_label(t: dict[str, Any], index: int) -> str:
    urgency = t.get("urgency", "?")
    cat = t.get("category", "")[:28]
    raw = (t.get("text_raw") or "")[:52].replace("\n", " ")
    suffix = "…" if len(raw) >= 52 else ""
    return f"{index + 1}. [{urgency}] {cat} — {raw}{suffix}"


def _render_ticket_detail(t: dict[str, Any]) -> None:
    st.subheader("Ticket details")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Score", f"{float(t.get('score', 0)):.4f}")
    with c2:
        st.metric("Urgency", str(t.get("urgency", "—")))
    with c3:
        st.metric("Queue target", str(t.get("queue_target", "—")))
    st.markdown(f"**Category:** `{t.get('category', '')}`")
    st.markdown(f"**Status:** `{t.get('status', '')}`")
    st.markdown(f"**ID:** `{t.get('id', '')}`")
    st.markdown(f"**Created at:** `{t.get('created_at', '')}`")
    with st.expander("Raw text", expanded=True):
        st.text(t.get("text_raw") or "")
    with st.expander("Processed text"):
        st.text(t.get("text_processed") or "")


def main() -> None:
    st.set_page_config(page_title="SmartTicket demo", layout="wide")
    st.title("SmartTicket — triage demo")
    st.caption(
        "Tickets are classified on the API, triaged (urgency + queue), persisted, "
        "and listed below in **API queue order**."
    )

    locked_base = _locked_api_base()
    if locked_base is not None:
        base = locked_base
        st.session_state.api_base = base
    else:
        if "api_base" not in st.session_state:
            st.session_state.api_base = initial_api_base()

    with st.sidebar:
        st.header("API")
        if locked_base is not None:
            src = (
                "app secret `SMARTTICKET_API_BASE_URL`"
                if _secret_api_base()
                else "environment `SMARTTICKET_API_BASE_URL` (Streamlit Cloud)"
            )
            st.caption(
                f"API base URL is **fixed** from {src} "
                "(visitors cannot point this app at arbitrary hosts — SSRF-safe)."
            )
            st.code(base, language="text")
        else:
            st.caption(
                "On **Streamlit Community Cloud**, set the secret `SMARTTICKET_API_BASE_URL` "
                "to your deployed API (https://…). Local dev: edit below or use "
                "`http://127.0.0.1:8000`."
            )
            typed = st.text_input(
                "Base URL", value=st.session_state.api_base, key="api_base_input"
            )
            st.session_state.api_base = typed.strip() or initial_api_base()
            base = st.session_state.api_base

        if st.button("Check health"):
            code, body = fetch_health(base)
            if code == 200 and isinstance(body, dict) and body.get("status") == "ready":
                st.success("API ready (model artifacts present).")
            elif code == 503:
                st.warning("API up but model **not_ready** — train/copy artifacts or check paths.")
            else:
                st.error(f"Health HTTP {code}: {_compact_api_error(code, body)}")

        st.divider()
        st.caption(
            "Human vs LLM routing uses **`SMARTTICKET_LLM_MIN_SCORE`** on the API host (see `.env.example`)."
        )

    if (
        _running_on_streamlit_cloud()
        and locked_base is None
        and _is_non_public_api_host(base)
    ):
        st.error(
            "This app is running on **Streamlit Community Cloud**, but the API base URL points "
            "to **localhost** (or another host the cloud cannot reach). "
            "Open **App settings → Secrets** and set `SMARTTICKET_API_BASE_URL` to your public "
            "**https://** FastAPI URL (no trailing slash). See `demo/README.md`."
        )
        st.stop()

    if _looks_like_railway_dashboard_url(base):
        st.warning(
            "**This base URL looks like the Railway project/dashboard**, not your FastAPI service. "
            "In Railway: select the **service** that runs uvicorn → **Settings** → **Networking** "
            "→ copy the **public URL** (usually `*.up.railway.app`). Put that full value in "
            "**Streamlit secrets** as `SMARTTICKET_API_BASE_URL` (no `/project/…`, no Postgres URL)."
        )

    col_submit, col_refresh = st.columns([4, 1])
    with col_submit:
        ticket_text = st.text_area(
            "New ticket text",
            height=160,
            placeholder="Describe the customer issue…",
            key="ticket_body",
        )
    with col_refresh:
        st.write("")
        st.write("")
        st.button("Refresh queues", type="secondary")

    submitted = st.button("Submit ticket → pipeline", type="primary")

    if submitted:
        if not (ticket_text or "").strip():
            st.warning("Enter some text before submitting.")
        else:
            code, body = submit_predict(base, ticket_text.strip())
            if code == 200 and isinstance(body, dict):
                st.success(
                    f"Stored. **Category:** `{body.get('category')}` · "
                    f"**Score:** {float(body.get('score', 0)):.4f} · "
                    f"**Urgency:** {body.get('urgency')} · "
                    f"**Queue:** **{body.get('queue_target')}**"
                )
            elif code == 503:
                st.error(f"API unavailable (database or model): {_compact_api_error(code, body)}")
            elif code == 422:
                st.error(f"Validation error: {body}")
            else:
                st.error(_compact_api_error(code, body))

    # Load queues (each rerun hits the API — same order as production)
    human_code, human_body = fetch_queue(base, "human")
    llm_code, llm_body = fetch_queue(base, "llm")

    err_cols = st.columns(2)
    if human_code != 200:
        with err_cols[0]:
            st.error(f"Human queue — {_compact_api_error(human_code, human_body)}")
    if llm_code != 200:
        with err_cols[1]:
            st.error(f"LLM queue — {_compact_api_error(llm_code, llm_body)}")

    human_items: list[dict[str, Any]] = []
    llm_items: list[dict[str, Any]] = []
    if human_code == 200 and isinstance(human_body, dict):
        human_items = human_body.get("items") or []
    if llm_code == 200 and isinstance(llm_body, dict):
        llm_items = llm_body.get("items") or []

    tab_human, tab_llm = st.tabs(
        [
            f"Human queue ({human_body.get('total', 0) if human_code == 200 else '—'})",
            f"LLM queue ({llm_body.get('total', 0) if llm_code == 200 else '—'})",
        ]
    )

    with tab_human:
        st.markdown("Ordering: **`GET /tickets?queue_target=human`** (HIGH → MEDIUM → LOW, then FIFO).")
        if not human_items:
            st.info("No tickets in the human queue.")
        else:
            labels = [_ticket_label(x, i) for i, x in enumerate(human_items)]
            choice_h = st.selectbox(
                "Select a ticket",
                options=list(range(len(human_items))),
                format_func=lambda i: labels[i],
                key="pick_human",
            )
            _render_ticket_detail(human_items[int(choice_h)])

    with tab_llm:
        st.markdown("Same ordering as **`GET /tickets?queue_target=llm`** (threshold on API).")
        if not llm_items:
            st.info("No tickets in the LLM queue.")
        else:
            labels_l = [_ticket_label(x, i) for i, x in enumerate(llm_items)]
            choice_l = st.selectbox(
                "Select a ticket",
                options=list(range(len(llm_items))),
                format_func=lambda i: labels_l[i],
                key="pick_llm",
            )
            _render_ticket_detail(llm_items[int(choice_l)])

    with st.expander("Debug: last queue responses"):
        st.json(
            {
                "human": human_body
                if human_code == 200
                else {"error": _compact_api_error(human_code, human_body)},
                "llm": llm_body
                if llm_code == 200
                else {"error": _compact_api_error(llm_code, llm_body)},
            }
        )


if __name__ == "__main__":
    main()
