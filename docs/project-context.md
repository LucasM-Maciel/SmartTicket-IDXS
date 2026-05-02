# Project Context
## SmartTicket — Operational Intelligence Platform for Customer Support

> Last updated: 2026-05-02
> Full product vision: see `docs/product-vision-pt.md` and `docs/product-vision-en.md`
>
> **Technical MVP (agreed scope):** **COMPLETE** as of **2026-05-02** (02/05) — see *Technical MVP closure — implementation status* below. *Produto funcional* (WhatsApp, UI, broker, LLM na resposta ao cliente) continua em roadmap, não neste marco.

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

Implemented on **`feature/api-mvp`** (merge history vs **`develop`**: **`branch-feature-api-mvp-vs-develop.md`**). Includes **`GET /health`**, **`POST /predict`**, **`GET /tickets`** (queue read, **`app/db/queue_repository.py`**), Pydantic + **`MAX_TICKET_TEXT_CHARS`**, env-based artifact paths, **`docs/api-contracts.md`**, **`docs/security-and-deployment.md`**, **`tests/test_api.py`**, **`tests/test_queue_api.py`**. **Persistence:** when **`DATABASE_URL`** is set, **`POST /predict`** writes **`tickets`** (`app/db/*`, **`tests/test_persistence.py`**, **`classify_ticket`** facade in **`app/services/classifier.py`**).

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

**Refund vs cancellation:** both map to `HIGH` urgency in the MVP policy below; keeping separate classifier labels (`refund_request` vs `cancellation_request`) preserves analytics and playbooks even though urgency is the same.

---

## Technical MVP closure — implementation status

This section records **agreed scope** for finishing the **technical MVP** after persistence. Identifiers in code and APIs are **English**.

**Closure statement:** o **MVP técnico** neste âmbito está **encerrado** (**data de fecho: 02/05/2026**): todos os critérios da tabela abaixo e do plano de dois PRs estão **implementados e testados** no repositório. Trabalho seguinte = **backlog de produto** (canais, fila operacional com broker, UI, detalhe/PATCH de ticket, auth, mensagens, LLM na resposta, etc.), não extensão do marco “technical MVP closure” aqui definido.

### What is new (final technical MVP increment)

Última entrega que **fecha** o MVP técnico (além do que já existia: pipeline, ML, `POST /predict`, persistência, triagem):

- **`GET /tickets`** — leitura paginada da fila persistida: ordem **HIGH → MEDIUM → LOW**, depois **FIFO** por `created_at`; filtro opcional `queue_target` (`human` | `llm`); respostas **503** / **422** conforme contrato.
- **`app/db/queue_repository.py`** — `list_tickets_queue` (SQL read-only, total + `limit`/`offset`).
- **Schemas** — `TicketQueueItem`, `TicketQueueResponse` em `app/api/schemas.py`.
- **Testes** — `tests/test_queue_api.py`; fixture partilhada **`sqlite_session_factory`** em `conftest.py` (raiz do repo).

*Referência de contrato:* `docs/api-contracts.md`. *Histórico de implementação da fila:* `docs/dev-log.md` (**2026-04-13**). *Data oficial de fecho do MVP técnico (âmbito acordado):* **2026-05-02** (02/05).

### Status (code in repo)

| Slice | Status | Where |
|-------|--------|--------|
| Urgency tiers + category mapping | **Shipped** | `app/services/ticket_triage.py` (`HIGH` / `MEDIUM` / `LOW`) |
| Score → human vs LLM **routing flag** | **Shipped** | `queue_target`: `human` \| `llm`; threshold **`SMARTTICKET_LLM_MIN_SCORE`** (`app/core/triage_settings.py`, default **0.75**) |
| Persist `urgency` + `queue_target` on `POST /predict` | **Shipped** | `app/db/models.py`, `app/db/repository.py`, `app/api/routes.py`, `PredictResponse` |
| PostgreSQL migration for existing DBs | **Shipped** | `db/migrations/001_add_urgency_queue_target.sql` |
| Broker / async consumer / RabbitMQ | **Not** in scope | Logical flags only |
| **Read** API: ordered queue... | **Shipped** | **`GET /tickets`** — `app/db/queue_repository.py`; tests **`tests/test_queue_api.py`** |

### Completion criteria (original two-PR plan)

| PR | Branch name (suggested) | Scope |
|---|---|---|
| **1** | `feature/mvp-urgency-logic` | ✅ Urgency + human/LLM routing fields, persistence on `POST /predict`, migration, env thresholds, **unit tests** (`test_ticket_triage.py`, `test_triage_settings.py`, persistence/API updates) |
| **2** | `feature/mvp-queue-api` | ✅ **`GET /tickets`** — order HIGH→MEDIUM→LOW then `created_at` ASC; query `queue_target`, `limit`, `offset`; **`TicketQueueResponse`**; **`test_queue_api`** |

Optional later (does **not** block technical MVP closure): small **Streamlit** UI for collaborators to exercise the API — see note at end of Development Order.

### Urgency levels (queue tiers)

Three tiers, ordered for servicing: **`HIGH` → `MEDIUM` → `LOW`**.

- **Between tiers:** work through **all `HIGH` tickets before any `MEDIUM`**, then all `MEDIUM` before **`LOW`** (strict tiered queue).
- **Within the same tier:** **FIFO** by arrival — first ticket created in that tier is answered first (`created_at` ascending as tie-break).

### Category → urgency (MVP)

Deterministic mapping from **predicted category** (model output string must match training labels — normalize casing/spacing if needed):

| Predicted category | Urgency |
|---|---|
| `technical_issue` | `MEDIUM` |
| `product_inquiry` | `MEDIUM` |
| `billing_inquiry` | `LOW` |
| `refund_request` | `HIGH` |
| `cancellation_request` | `HIGH` |

Unknown or unexpected categories: define an explicit fallback (e.g. `MEDIUM` or `LOW`) in code and tests.

### Human vs LLM routing (confidence split)

Separate from urgency: route by **classification score** from `predict_category`:

- **Low score** → **human** queue (low confidence in the predicted label).
- **High score** → **LLM** queue (high confidence).

Threshold(s) live in **environment variables** (e.g. a single `SMARTTICKET_LLM_MIN_SCORE`) with conservative defaults until real data calibration. Document in `.env.example`.

### Explicitly **not** in technical MVP closure

- **Priority aging** (e.g. `MEDIUM` promoting to `HIGH` after wait time).
- **Manual urgency override** by agents (downgrade false alarms, etc.).
- **Review queue** after LLM replies (human feedback / enrichment) — third workflow axis.
- **RabbitMQ** — logical queue in PostgreSQL + API is enough for this milestone.

These remain **product backlog** after the technical MVP ships.

---

## Development Order

### MVP (target: end of April 2026)

**Pipeline + prediction model — complete as of 2026-04-11:** preprocessing, training (`train_model`), inference (`predict_category`), ML unit tests, and repo-root pytest wrappers (`scripts/retest.*`).

**API + persistence + triage + queue read — implemented:** `GET /health`, `POST /predict`, **`GET /tickets`** (paginated, ordered queue), schemas **`TicketQueueItem`** / **`TicketQueueResponse`**, **`list_tickets_queue`**, tests **`test_queue_api`**, root **`conftest.py`** fixture **`sqlite_session_factory`**. Merge/git bookkeeping: **`docs/branch-feature-api-mvp-vs-develop.md`**.

1. ✅ Data pipeline (cleaning + normalization)
2. ✅ ML classification (TF-IDF + Logistic Regression)
3. ✅ Model training + artifacts saved (`python -m app.ml.train`)
4. ✅ `predict_category` in `app/ml/predict_category.py` (category + score)
5. ✅ Edge case handling in predict — empty / blank preprocessed text → `unknown` / `0.0` (`predict_category`); short text still goes through model
6. ✅ Unit tests — utils, pipeline, `train`, `predict_category`
7. ✅ FastAPI routes — `GET /health`, `POST /predict`, **`GET /tickets`** + Pydantic schemas *(merge into `develop` may lag — verify with git)*
8. ✅ HTTP tests — `tests/test_api.py`, **`tests/test_persistence.py`**, **`tests/test_queue_api.py`** (`TestClient` / SQLite overrides)
9. ✅ Minimal **`tickets`** persistence (`DATABASE_URL`, SQLAlchemy) — contacts/messages/extended ticket columns **still open**
10. ✅ **Urgency + `queue_target`** on `POST /predict` (triage module, env threshold, SQL migration, tests)
11. ✅ **`GET /tickets`** queue list (tier order + FIFO, filter `queue_target`, pagination)
12. ⏳ Full product E2E (channels → API → persist **→ attendant UI**, WhatsApp, etc.)

### Post-MVP
13. ⏳ WhatsApp integration
14. ⏳ Agent interface (Streamlit for demo, React for production)
15. ⏳ LLM integration (full response path beyond routing flags)
16. ⏳ Priority aging + manual urgency overrides + review queue (LLM → human feedback)
17. ⏳ Feedback loop + automatic retraining
18. ⏳ Monthly analytics report

### Note — optional validation UI before full product MVP

Building a small **Streamlit** screen is optional to let collaborators test the pipeline and queue behavior; it is **not required** to close the technical MVP scope in *Technical MVP closure — implementation status*.

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
