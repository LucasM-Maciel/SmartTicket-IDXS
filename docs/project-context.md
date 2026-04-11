# Project Context
## SmartTicket — Operational Intelligence Platform for Customer Support

> Last updated: 2026-04-11
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

### Full product MVP (target: end of April 2026)

What the shipped product must include for the first release:
- ML-backed classification (category + confidence) exposed through the API
- API calling the pipeline (`POST /predict`)
- `POST /health` endpoint with model load status
- Database persistence (tickets, contacts, messages)
- Preprocessing pipeline integrated with the HTTP layer
- Edge case handling in predict (empty text, None, very short input), enforced end-to-end once routes exist
- Model training via `python -m app.ml.train` (writes artifacts under `artifacts/`)
- Automated tests including API coverage when FastAPI routes are implemented

### Completed technical slice (2026-04-11)

Delivered by the pipeline/ML track **before** API + DB integration. In scope: **text → preprocess → offline train → offline infer → unit tests**. Not in scope: persisting tickets or predictions after classification, or any HTTP surface.

- Preprocessing pipeline working independently (`clean_text` → `normalize_text` → `run_pipeline`)
- ML model classifying tickets offline (`train_model`, `predict_category`, `joblib` artifacts)
- Edge case handling in `predict_category` (empty / blank preprocessed text → `unknown` / `0.0`)
- Unit tests: pipeline, preprocessing, ML train/predict (`tests/test_api.py` placeholder until FastAPI exists)
- Convenience test runners: `scripts/retest.ps1` / `scripts/retest.bat` (see `scripts/retest.md`)

---

## Key Decisions

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

**Pipeline + prediction model (Lucas) — complete as of 2026-04-11:** preprocessing, training (`train_model`), inference (`predict_category`), ML unit tests, and repo-root pytest wrappers (`scripts/retest.*`). This milestone is **only** the text → model path; it does **not** include saving tickets or predictions to a database after classification (that requires the FastAPI + persistence track).

**`tests/test_api.py`** remains a placeholder until the FastAPI app exists; API tests ship with that work.

1. ✅ Data pipeline (cleaning + normalization)
2. ✅ ML classification (TF-IDF + Logistic Regression)
3. ✅ Model training + artifacts saved (`python -m app.ml.train`)
4. ✅ `predict_category` in `app/ml/predict_category.py` (category + score)
5. ✅ Edge case handling in predict — empty / blank preprocessed text → `unknown` / `0.0` (`predict_category`); short text still goes through model
6. ✅ Unit tests — utils, pipeline, `train`, `predict_category` (API tests pending with FastAPI)
7. ⏳ FastAPI app + POST /predict + POST /health (Salim)
8. ⏳ Request/response schemas + validation (Salim)
9. ⏳ Database persistence — CONTACTS, TICKETS, MESSAGES (Salim)
10. ⏳ End-to-end validation (input → predict → persist → response)

### Post-MVP
11. ⏳ WhatsApp integration
12. ⏳ Agent interface (Streamlit for demo, React for production)
13. ⏳ LLM integration
14. ⏳ Priority aging + queue
15. ⏳ Feedback loop + automatic retraining
16. ⏳ Monthly analytics report

---

## Timeline

| Phase | Period | Goal |
|---|---|---|
| Technical MVP | Now → April 2026 | Classification + API working |
| Demo | May–June 2026 | Full system for pilot client demo |
| Refinement | July–September 2026 | Queue + interface + WhatsApp + full DB |
| Pilot deployment | October 2026 | First real client |
| Scale | 2027 | 5–10 clients |
