# Project Context
## SmartTicket — Operational Intelligence Platform for Customer Support

> Last updated: 10/04/2026
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

## MVP Definition

The MVP includes:
- Preprocessing pipeline working independently
- ML model classifying tickets (category + confidence score)
- API calling the pipeline (`POST /predict`)
- `POST /health` endpoint with model load status
- Database persistence (tickets, contacts, messages)
- Edge case handling in predict (empty text, None, very short input)
- Model training via `python -m app.ml.train` (writes artifacts under `artifacts/`)
- Unit tests: pipeline, preprocessing, ML train/predict (`tests/test_api.py` placeholder until FastAPI exists)

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

**Pipeline + prediction model (Lucas):** preprocessing, training, `predict_category`, and ML unit tests are in place for this slice. **`tests/test_api.py`** is intentionally empty until the FastAPI app lands; API tests will be added with that work.

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
12. ⏳ WhatsApp integration
13. ⏳ Agent interface (Streamlit for demo, React for production)
14. ⏳ LLM integration
15. ⏳ Priority aging + queue
16. ⏳ Feedback loop + automatic retraining
17. ⏳ Monthly analytics report

---

## Timeline

| Phase | Period | Goal |
|---|---|---|
| Technical MVP | Now → April 2026 | Classification + API working |
| Demo | May–June 2026 | Full system for pilot client demo |
| Refinement | July–September 2026 | Queue + interface + WhatsApp + full DB |
| Pilot deployment | October 2026 | First real client |
| Scale | 2027 | 5–10 clients |
