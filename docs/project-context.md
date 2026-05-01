# Project Context
## SmartTicket — Operational Intelligence Platform for Customer Support

> Last updated: 2026-04-24
> Full product vision: see `docs/product-vision-pt.md` and `docs/product-vision-en.md`

---

## Product

SmartTicket is an **operational intelligence platform for customer support** that combines Machine Learning, LLMs, and automation to classify, prioritize, and resolve support tickets — reducing the human team's workload and generating business intelligence from every interaction.

---

## Problem

Companies receiving medium-to-high volumes of customer messages struggle to:
- Classify requests automatically
- Prioritize urgent tickets over less urgent ones
- Respond efficiently without overloading agents
- Extract intelligence from historical interactions
- Measure and improve their support operation over time

---

## Solution

```
WhatsApp → Preprocessing Pipeline → ML Classification → LLM auto-resolve
                                                              ↓
                                                    Human queue (if needed)
                                                              ↓
                                                  Agent responds via interface
                                                              ↓
                                              Everything stored → analytics + retraining
```

---

## MVP definition

### Ownership of what is shipped today

The **technical MVP to date** (pipeline, ML, FastAPI routes, **PostgreSQL persistence path**, tests, and related docs) is **implemented entirely by Lucas**. Nothing in that deliverable is authored or owned by other team members (Salim, Rafael, Luís, etc.); their roles in `docs/team-responsibilities.md` describe **planned or future** collaboration, not contributions to this codebase slice.

### Full product MVP (target: end of April 2026)

What the shipped product must include for the first release:
- ML-backed classification (category + confidence) exposed through the API
- API calling the pipeline (`POST /predict`)
- `GET /health` endpoint with model load status
- Database persistence — **`tickets` rows today** (`DATABASE_URL`, SQLAlchemy); **contacts/messages** and extended ticket fields still to ship for full MVP
- Preprocessing pipeline integrated with the HTTP layer
- Edge case handling in predict (empty text, None, very short input), enforced on **`POST /predict`**
- Model training via `python -m app.ml.train` (writes artifacts under `artifacts/`)
- Automated tests including API coverage when FastAPI routes are implemented

### Completed technical slice — pipeline + ML (2026-04-11)

Delivered by the pipeline/ML track **before** API/database integration (*historical milestone — 2026-04-11*). In scope: **text → preprocess → offline train → offline infer → unit tests**. Not in scope *for that slice alone*: persisting tickets or predictions after classification. **Current stack:** persistence on `POST /predict` when `DATABASE_URL` is set — see *API technical MVP* below.

- Preprocessing pipeline working independently (`clean_text` → `normalize_text` → `run_pipeline`)
- ML model classifying tickets offline (`train_model`, `predict_category`, `joblib` artifacts)
- Edge case handling in `predict_category` (empty / blank preprocessed text → `unknown` / `0.0`)
- Unit tests: pipeline, preprocessing, ML train/predict
- Convenience test runners: `scripts/retest.ps1` / `scripts/retest.bat` (see `scripts/retest.md`)

### API technical MVP (`feature/api-mvp` vs `develop`)

Implemented on **`feature/api-mvp`** (merge history vs **`develop`**: **`branch-feature-api-mvp-vs-develop.md`**). Includes **`GET /health`**, **`POST /predict`**, Pydantic + **`MAX_TICKET_TEXT_CHARS`**, env-based artifact paths, **`docs/api-contracts.md`**, **`docs/security-and-deployment.md`**, **`tests/test_api.py`**. **Persistence:** when **`DATABASE_URL`** is set, **`POST /predict`** writes **`tickets`** (`app/db/*`, **`tests/test_persistence.py`**, **`classify_ticket`** facade in **`app/services/classifier.py`**).

---

## Key Decisions

**Data / persistence:**
- **PostgreSQL** is the agreed relational database (technical MVP through final product; not SQLite as the long-term default).

**ML:**
- TF-IDF + Logistic Regression (baseline)
- No deep learning for MVP
- No RAG for MVP
- Classification on accumulated messages if first message score is low (< 0.75)

**Product:**
- Agent responds exclusively through SmartTicket interface (never directly via WhatsApp)
- System sends responses via WhatsApp Business API in the background
- Priority aging: ticket priority increases automatically with waiting time
- Human-in-the-loop: LLM resolves simple cases, humans handle the rest
- Feedback loop: agent corrections feed model retraining

**Business:**
- Pricing: R$3,000 setup + R$500/month (up to 600 tickets)
- LLM and WhatsApp API costs passed to client
- Pilot validation client already confirmed

---

## Categories (MVP — simplified for development)

- `technical_issue` — technical problems with product/service
- `billing_inquiry` — billing questions or issues
- `refund_request` — refund requests
- `cancellation_request` — cancellation requests
- `product_inquiry` — product or service questions

> In the real product, categories are defined per client after analysis of their historical tickets.
> Similar categories are consolidated, low-volume ones may be grouped.
> Final count can easily exceed 10 categories depending on the business.
> The model is retrained for each client's category configuration.

---

## Development Order

### MVP (target: end of April 2026)

**Pipeline + prediction model — complete as of 2026-04-11:** preprocessing, training (`train_model`), inference (`predict_category`), ML unit tests, and repo-root pytest wrappers (`scripts/retest.*`).

**API + persistence — implemented:** `GET /health`, `POST /predict`, schemas, limits, 503/422 behavior, **`classify_ticket`**, **`app/db`** (`Ticket`, **`DATABASE_URL`**), **`tests/test_api`** + **`tests/test_persistence`**. Merge/git bookkeeping vs **`develop`**: **`docs/branch-feature-api-mvp-vs-develop.md`**.

1. ✅ Data pipeline (cleaning + normalization)
2. ✅ ML classification (TF-IDF + Logistic Regression)
3. ✅ Model training + artifacts saved (`python -m app.ml.train`)
4. ✅ `predict_category` in `app/ml/predict_category.py` (category + score)
5. ✅ Edge case handling in predict — empty / blank preprocessed text → `unknown` / `0.0` (`predict_category`); short text still goes through model
6. ✅ Unit tests — utils, pipeline, `train`, `predict_category`
7. ✅ FastAPI routes — `GET /health`, `POST /predict` + Pydantic schemas *(merge into `develop` may lag — verify with git)*
8. ✅ HTTP tests — `tests/test_api.py`, **`tests/test_persistence.py`** (`TestClient`, dependency overrides)
9. ✅ Minimal **`tickets`** persistence (`DATABASE_URL`, SQLAlchemy) — contacts/messages/extended ticket columns **still open**
10. ⏳ Full product E2E (channels → API → persist **→ reads/UI**, urgency, queue)

### Post-MVP
11. ⏳ WhatsApp integration
12. ⏳ Agent interface (Streamlit for demo, React for production)
13. ⏳ LLM integration
14. ⏳ Priority aging + queue
15. ⏳ Feedback loop + automatic retraining
16. ⏳ Monthly analytics report

---

## Future technical planning

Directions **after** the core product path (API, DB, feedback loop) is stable — not MVP commitments; revisit when pain appears.

**MLOps & orchestration**
- **MLflow** (or equivalent): consider when multiple experiments, model versions, and metric comparison become routine — less urgent while training stays a simple baseline and artifacts are few.
- **Apache Airflow** (or lighter options: cron, CI schedules, cloud schedulers): consider when retraining and data pipelines need **DAGs**, retries, and operational monitoring; avoid the operational cost until scheduled jobs are a real requirement.

**LLM & retrieval**
- **RAG / embeddings / vector store**: consider when auto-responses must be **grounded in client knowledge** (policies, KB, long docs) and prompt-only LLM is insufficient; not required for MVP classification + simple LLM flows.

**Analytics & visualization**
- **BI** (e.g. Power BI, Metabase, Looker-style tools) on **SQL** over the operational DB or warehouse: primary path for business-facing dashboards and self-serve exploration.
- **Python** (notebooks, Streamlit/Dash, or chart libs): keep for **data prep**, ad-hoc analysis, ML evaluation, and **embedded** internal tools where a full BI stack is overkill.
- Typical pattern: **hybrid** — metrics layer in SQL/Python, consumption in BI; productized views only where needed.

---

## Timeline

| Phase | Period | Goal |
|---|---|---|
| Technical MVP | Now → April 2026 | Classification + API working |
| Demo | May–June 2026 | Full system for pilot client demo |
| Refinement | July–September 2026 | Queue + interface + WhatsApp + full DB |
| Pilot deployment | October 2026 | First real client |
| Scale | 2027 | 5–10 clients |
