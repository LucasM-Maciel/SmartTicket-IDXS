# 🧠 Intelligent Triage System

> End-to-end intelligent system for classifying, processing, and learning from customer tickets using Machine Learning and LLMs.

<p align="center">
  <b>Built with real-world architecture principles • Scalable • Modular • Production-oriented</b>
</p>

---

## 🚀 Overview

The **Intelligent Triage System** is a production-oriented application designed to process and understand unstructured text data such as support tickets, user requests, and operational messages.

It combines:

- 🧠 **Machine Learning** → structured classification
- 🤖 **LLMs (planned)** → contextual and human-like responses
- ⚙️ **Data Pipelines** → robust preprocessing and transformation
- 📊 **Data Layer** → analytics, monitoring, and continuous improvement

---

### 🎯 Goal

Transform raw text into:

- 📌 Category (intent)
- 📊 Confidence score
- ⚠️ *(Future)* Priority (urgency)
- 💬 *(Future)* Automated response

While also enabling:

- 📈 Business insights
- 🔁 Continuous learning
- ⚙️ Operational optimization

---

## 🏗️ System Architecture

### 🔵 Online Flow (Real-Time Inference)

```text
Customer sends message on WhatsApp
↓
WhatsApp Business API → webhook
↓
FastAPI: validate + save contact/ticket
↓
Text Preprocessing Pipeline (clean → normalize → vectorize)
↓
ML Model (TF-IDF + Logistic Regression)
↓
Category + Confidence Score
↓
Score ≥ 0.75?
├─ Yes → LLM attempts resolution → resolved or escalated
└─ No  → Human queue (low confidence)
↓
Agent responds via SmartTicket interface
↓
System delivers response via WhatsApp API
↓
Everything stored → analytics + model retraining
```

---

### 🟢 Offline Flow (Training Pipeline)

```text
Raw Data
↓
Data Cleaning & Normalization
↓
Feature Engineering
↓
Model Training
↓
Evaluation (Metrics)
↓
Model Persistence
```

---

## 🧩 Core Components

### 📦 Data Pipeline

- Text normalization
- Stop-word removal *(if enabled)*
- Token standardization
- Noise reduction (punctuation, casing, etc.)

---

### 🧠 Machine Learning Layer

- **Vectorization:** TF-IDF
- **Model:** Logistic Regression

**Current Output:**

- Category classification
- Confidence score

**Planned:**

- Priority classification (multi-output or secondary model)

---

### 🤖 LLM Layer *(Planned)*

The LLM layer is designed to operate with **structured context from the ML model**, not as a standalone black box.

Instead of relying only on raw input, the LLM receives:

- Predicted category
- Confidence score
- *(Future)* Priority level

This hybrid approach ensures:

- Higher response accuracy
- Reduced hallucination risk
- More controlled and consistent outputs
- Better alignment with business logic

#### Example Flow

```text
User message
→ ML classification
→ Context injection (category + score)
→ LLM response generation
```

---

### 🌐 API Layer

- Built with **FastAPI**
- RESTful architecture (initial version simplified)

**Current endpoints:**

```http
GET /health
POST /predict
```

Handles:

- Input validation
- Classification via `app/services/classifier.classify_ticket` (wraps `predict_category`)
- **Persistence:** inserts one **`tickets`** row (`text_raw`, `text_processed`, `category`, `score`, …) when `DATABASE_URL` is set — otherwise **`POST /predict`** returns **503** (`Database persistence not configured.`)
- Response formatting

---

### 🗃️ Data Layer *(partial — MVP persistence)*

- **PostgreSQL** in deployments via **`DATABASE_URL`** (SQLAlchemy + `psycopg2-binary`; see `app/db/session.py`, `app/db/models.py`)
- **`tickets` table:** UUID PK, raw/processed text, category, score, status (`classified`), `created_at`
- **Tests:** SQLite file DB via dependency overrides (`tests/test_persistence.py`) — no impact from a developer’s local `.env` thanks to `conftest.py` clearing `DATABASE_URL`

Contacts/messages schema and read/query APIs remain **planned** (see `docs/architecture.md`).

---

## 📊 Data & Analytics Layer

The system is not only designed for real-time inference but also for **data collection and intelligence generation**.

Each interaction may store:

- Raw input text
- Processed text
- Predicted category
- Confidence score
- *(Future)* Priority
- *(Future)* LLM-generated response
- Timestamps and metadata
- *(Future)* Human-validated outcomes

---

### 🎯 Purpose

This enables:

- 📈 Business analytics
  - Most frequent issues
  - Demand peaks
  - Category distribution

- 🧠 Continuous model improvement
  - Retraining with real-world data
  - Error correction

- 🔍 Model evaluation and auditing

- ⚙️ Operational insights
  - Support team optimization
  - SLA improvements

---

### 🔁 Feedback Loop

The system evolves through a continuous learning cycle:

1. Collect real interactions
2. Store predictions and outcomes
3. Compare predicted vs actual results
4. Improve model and prompts
5. Redeploy improved versions

---

## ⚙️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| Data Processing | Pandas |
| ML | Scikit-learn (TF-IDF + Logistic Regression) |
| API | FastAPI |
| Database | PostgreSQL — Supabase (MVP), Railway/RDS (production) |
| LLM | OpenAI API *(planned)* |
| WhatsApp | Z-API / Twilio *(planned)* |
| Real-time | WebSockets via FastAPI — polling for demo |
| Agent Interface | Streamlit (demo) → React / Next.js (production) |
| Scheduled Jobs | APScheduler *(planned)* |
| ORM / DB driver | SQLAlchemy · psycopg2-binary |
| LLM libraries *(deps present; integration stub)* | openai · langchain (`app/services/llm_service.py` placeholder) |
| Version Control | Git & GitHub |

---

## 📡 API Contract (Current)

The `text` field is capped for API safety; see `app/core/limits.py` and `docs/api-contracts.md`.

### 📥 Request

```json
{
  "text": "I want to cancel my order"
}
```

---

### 📤 Response

```json
{
  "text": "I want to cancel my order",
  "category": "cancellation",
  "score": 0.92
}
```

---

## 📊 Features

### ✅ Current

- 🔄 Text preprocessing pipeline (`clean_text` → `normalize_text` → `run_pipeline`)
- 🧠 TF-IDF + Logistic Regression model (training + inference implemented)
- 📦 Model and vectorizer persistence via `joblib`
- 🌐 Multilingual pipeline support (`language` parameter, English default)
- 🧪 Pytest coverage for preprocessing, normalizer, pipeline, training, and `predict_category` (`tests/` — strategy in `docs/test-plan.md`, tips in `tests/best_practices.md`)
- Test runners `scripts/retest.ps1` / `scripts/retest.bat` — invoke pytest from repo root (see `scripts/retest.md`)
- **MVP slice (2026-04-11):** pipeline + training + `predict_category` is complete (DB persistence was out of scope for that slice only).
- **API + persistence:** `GET /health`, `POST /predict`, Pydantic limits; ticket row written when `DATABASE_URL` is set (`app/db/`, `tests/test_api.py`, `tests/test_persistence.py`) — see `docs/api-contracts.md` and `docs/branch-feature-api-mvp-vs-develop.md`

---

### 🚧 In Progress

- Merge ongoing feature branches to `develop` as PRs are approved (see `docs/branch-feature-api-mvp-vs-develop.md` when comparing historical deltas)
- Real-world dataset sourcing (current dataset is synthetic)
- Model evaluation with reliable data
- Contacts/messages schema, urgency field, priority queue, channels/UI (beyond classify + persist one row)

---

### 🔮 Planned

- Operational retrain entry point (e.g. `scripts/retrain.py`) when the feedback-loop / scheduling milestone lands
- 🤖 LLM automatic resolution (with structured ML context)
- ⚠️ Dynamic priority + priority aging queue
- 📱 WhatsApp Business API integration (Z-API / Twilio)
- 🖥️ Agent interface (Streamlit demo → React production)
- 🔁 Feedback loop + automatic model retraining (may include scheduled retrain jobs)
- 📈 Monthly analytics report
- ☁️ Cloud deployment

---

## 📈 Model Evaluation

> First training run completed. Metrics are not yet reliable — current dataset is synthetic and ticket descriptions have no clear semantic relationship with the labels.

Planned metrics:

- Accuracy
- Precision / Recall / F1-score
- Confusion matrix
- Business-oriented metrics (resolution success, response time)

> ⚠️ Evaluation will be meaningful only after replacing the dataset with real-world data.

---

<a id="smartticket-mvp-checklists"></a>
## 📋 Checklists: Technical MVP · Functional MVP · Final product

> **Key (GitHub):** the *Done* column uses ✅/⬜; lines with `- [ ]` / `- [x]` are native *task lists* (renders as checkboxes in the repository view). Target database: **PostgreSQL**. **Technical MVP** — *Technical SmartTicket MVP* (flow: test dataset → modular API → pipeline → prediction → priority queue → DB). **Functional MVP** — *Smart Ticket Architecture* / *Functional MVP* (WhatsApp → *cloud* → Ingestion → model + LLM + queue + DB → UI). **Final product** — same diagram family, with **Ingest/Query** split, **RabbitMQ** for the queue, LLM, and clearer data consumption (current vision below); business/roadmap detail: `docs/product-vision-en.md` / `docs/product-vision-pt.md`.

### 1) Technical MVP (*Technical SmartTicket MVP — diagram*)

| Done | Deliverable | Notes |
|:-----:|--------------|--------|
| ✅ | **PostgreSQL** as the target RDBMS | `DATABASE_URL` + SQLAlchemy; table `tickets` (see `app/db/models.py`) |
| ✅ | **Test dataset** (synthetic tickets / sample) | CSV + test requests with body `{"text": "…"}` on `POST /predict` |
| ✅ | Modular **SmartTicket API** (FastAPI) | `GET /health`, `POST /predict` — see `docs/api-contracts.md` |
| ✅ | **Preprocessing** (pipeline) | `clean_text` → `normalize_text` → `run_pipeline` |
| ✅ | **Prediction model** — classification + *score* | `predict_category`, TF-IDF + logistic regression; `joblib` artifacts |
| ⬜ | **Urgency** in the API flow → persist with classification + *score* | Not yet exposed/derived beyond class + *score* in the minimal contract |
| ⬜ | **Priority queue** (ordered by urgency) | Diagram: *Priority queue*; not implemented in the current API |
| ✅ | **PostgreSQL** — persist *ticket* + classification + *score* | `POST /predict` persists when `DATABASE_URL` is set (`save_ticket_prediction`); **503** if unset or write fails |
| ✅ | Limits, tests, security and contract docs | `app.core.limits`, `tests/test_api.py`, `docs/security-and-deployment.md` |

**Task list (for Git/PRs; mirrors the table):**

- [x] Test dataset + HTTP test calls (body with `text`)
- [x] Modular FastAPI (`/health`, `/predict`)
- [x] Preprocessing
- [x] Model: category + *confidence score*
- [ ] Urgency wired into the persistence path (as in the diagram)
- [ ] Priority queue (*priority queue* by urgency)
- [x] PostgreSQL: persist ticket + classification + *score* (requires `DATABASE_URL` + schema)
- [x] `MAX_TICKET_TEXT_CHARS` aligned train ↔ API; API tests; documentation

### 2) Functional MVP (*Smart Ticket Architecture / Functional MVP*)

As in the diagrams: **Ticket owner** (WhatsApp) → **WhatsApp API (BSP)** / **webhook** → **LB** → **API SmartTicket Ingestion**; in the *cloud* — **Model** (preprocessing, classification, *score*, urgency), **LLM** (*score*/classification context), **queue** (*Postgres* + *APScheduler* / urgency-prioritized), **DB**; **SmartTicket Interface Beta** (agent) and closed loop (LLM or agent response).

| Done | Deliverable | Notes |
|:-----:|------------|--------|
| ⬜ | **Ingress** — WhatsApp app → **BSP** → **webhook** → **load balancer** → tickets into ingestion | Not in the repo yet |
| ⬜ | **API SmartTicket Ingestion** (orchestrates: model, LLM, queue, persistence, UI) | Today: partial core = FastAPI with `GET /health` and `POST /predict` (no webhooks, no channel integration) |
| ⬜ | **Prediction model** — pipeline; output with **classification + *score* + urgency** (and in diagram variants, *entity extraction* / *degree to match*) | Today: category + *score*; urgency/entity not in the full path yet |
| ⬜ | **LLM provider** (OpenAI / Anthropic, etc.) — *Raw ticket* + *score* / classification (context) → **LLM response** | ML+LLM hybrid planned; not integrated in code |
| ⬜ | **Queue & scheduling** — *Postgres* + **APScheduler** (or multi-queue logic) — *prioritized by urgency score* | Diagram: queue; not implemented |
| ⬜ | **DB** — *read*; *write* ticket + classification + (urgency / queue) + agent reply; variant: persist “raw + model output” | **Write path** for classify + score exists (`tickets`); list/UI reads and urgency not implemented yet |
| ⬜ | **UI** — *SmartTicket Interface Beta*; **agent**; *data consuming* from Ingestion | Not in the repo |
| ⬜ | **User response** — *LLM* or agent (and *status* / *feedback* to the ticket owner) | Out of scope for the current MVP |

**Functional MVP task list:**

- [ ] Ingress: WhatsApp → BSP / webhook / LB → tickets into ingestion
- [ ] Ingestion API end-to-end (today: isolated HTTP *predict* only)
- [ ] Model: classification + *score* + **urgency** (and entity if applicable) in the same path as the rest of the system
- [ ] **LLM:** request with ticket + context (*score* / classification) → response
- [ ] Queue: *Postgres* + *APScheduler* (or equivalent) — **urgency**-based priority
- [ ] **PostgreSQL:** persist ticket, model outputs, queue/urgency, replies; reads for the API and UI
- [ ] **UI** (agent, Interface Beta) + data consumption from Ingestion
- [ ] Close the loop: response or *feedback* to the **ticket owner** (LLM and/or agent)

### 3) Final product (Smart Ticket Architecture, final-vision — current state in diagrams)

Step beyond functional MVP: **two services** (ingest vs. query), an explicit **RabbitMQ** message queue, and **LLM** on the **Query API** (UI-aligned integration). Overall flow: **Ticket owner** ↔ **WhatsApp** ↔ **BSP** ↔ **webhook** / **load balancer**; in the *cloud* — **API SmartTicket Ingestion** (Docker) coordinates the **model** (preprocessing → classification + *score* + urgency), **queue** (*Priority queue* with **RabbitMQ**), and **writes** to the **DB**; **API SmartTicket Query** (Docker) **reads** the DB, calls the **LLM** (*raw ticket* + *score* / classification) and feeds the **UI** (*data consuming*); persistence and egress include **agent messages**, **LLM draft**, and **replies** back to the channel (LLM and/or agent, including *Attendant or LLM response* / *Write messages…* in the diagram).

| Done | Deliverable | Notes |
|:-----:|------------|--------|
| ⬜ | **Edge ingress & egress** — *Ticket* and *LLM or attendant answer*; **BSP**; **webhook**; **LB**; *Read database*; message response/write on the WhatsApp path | Bidirectional flow in the design; not implemented in the repo |
| ⬜ | **API SmartTicket Ingestion** (container) — *Tickets* → model, queue, DB; write: persist *ticket* + *classification* + *score* + *urgency*; *persist attendant messages* (label variants in diagrams) | Current base: `POST /predict` with no real channel ingestion |
| ⬜ | **Prediction model** in the path (preprocessing ↔ classification, *score*, urgency) | *Score* + category in code; integrate and persist urgency |
| ⬜ | **Priority queue (RabbitMQ)** — *Urgency* in → *prioritized by urgency* out, wired to Ingestion | In final-product diagrams; not in the repo |
| ⬜ | **PostgreSQL** — full *read* / *write*: ticket, classification, *score*, urgency, work queue, messages; *Write: messages / LLM draft / attendant reply* (persistence/egress path) | Reconcile schema and contracts with `docs/architecture.md` |
| ⬜ | **API SmartTicket Query** (container) — DB read, **LLM** (*raw ticket* + *score* + *classification* as context → *LLM response*), *Data consuming* for the **UI** | Query API separate from ingestion |
| ⬜ | **UI** — *SmartTicket Interface* (purple layer); agent; consumes **Query** (not Ingestion alone) | Front end not in the repo |
| ⬜ | **Operations** — Docker (both services), *secrets*, observability, *hardening*; align with `docs/security-and-deployment.md` and product vision | See docs for detail |

**Final product task list:**

- [ ] Channel edge: Ticket owner ↔ **WhatsApp** ↔ **BSP** ↔ **webhook** / **LB**; **response** (LLM and/or agent) and *feedback*
- [ ] **Ingestion** (Docker): tickets → **pre-processing** → **model** → classification + *score* + **urgency** → **RabbitMQ** (*priority by urgency*) → **writes** to the DB
- [ ] **PostgreSQL:** combined ticket+ML+urgency; **messages** (agent, LLM draft); reads for Query
- [ ] **Query** (Docker): **read** the DB; **LLM** with context (*score* + classification); *Data consuming* → **UI**
- [ ] **UI** (Interface) + agent; response *loop* and persistence as in the diagrams
- [ ] **Product / business** (KPI, analytics, multi-channel, etc.) — `docs/product-vision-en.md` / `docs/product-vision-pt.md`

---

## 🛠️ Setup

### 1. Clone

```bash
git clone https://github.com/LucasM-Maciel/SmartTicket-IDXS.git
cd SmartTicket-IDXS
```

---

### 2. Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Train the model (writes `artifacts/`)

From the **repository root** (with your venv activated):

```bash
python -m app.ml.train
```

---

### 5. Run tests

From the **repository root**:

```bash
python -m pytest
```

On Windows you can use the wrappers (same effect, forwards extra args to pytest):

```powershell
.\scripts\retest.ps1
```

```bat
scripts\retest.bat
```

See `scripts/retest.md` for details.

---

### 6. Configure database *(required for successful `POST /predict`)*

Set **`DATABASE_URL`** for the API process (see `.env.example`). Create the **`tickets`** table before calling predict — from repo root, with SQLAlchemy metadata:

```bash
python -c "from app.db.models import Base; from app.db.session import get_engine; e=get_engine(); Base.metadata.create_all(bind=e) if e else print('Set DATABASE_URL')"
```

*(Production migrations may later move to Alembic — not in repo yet.)*

---

### 7. Run API

```bash
uvicorn app.main:app --reload
```

Endpoints: `GET /health` (artifact readiness), `POST /predict` (JSON `{"text":"…"}` — **503** if DB not configured or write fails). Details: `docs/api-contracts.md`.

**Manual smoke:** `python scripts/post_test_ticket.py` (needs running server + `DATABASE_URL`).

---

## 🗺️ Roadmap

### 🔹 MVP

- [x] Preprocessing pipeline
- [x] ML classification model (train + `predict_category`)
- [x] API surface (`GET /health`, `POST /predict`)
- [x] Persist predictions to **`tickets`** when `DATABASE_URL` is set (`app/db/*`, `tests/test_persistence.py`)

---

### 🔹 Next

- [ ] API versioning
- [ ] Model improvements
- [ ] Modular architecture (routers per ingestion vs query — see ADR `docs/adr/0001-…`)
- [ ] Schema expansions: contacts, messages, urgency; read/query endpoints

---

### 🔹 Future

- [ ] LLM integration *(stub module present; not wired to routes)*
- [ ] Monitoring & observability
- [ ] Multi-tenant system
- [ ] Cloud deployment

---

## 📄 Documentation

- **Index of all docs** → `docs/README.md`
- System Architecture → `docs/architecture.md` (Excalidraw interactive link: `docs/diagrams/README.md`)
- API Contracts → `docs/api-contracts.md`
- Security & deployment (MVP) → `docs/security-and-deployment.md`
- ML Notes → `docs/ml-notes.md`
- Test Plan → `docs/test-plan.md`
- Running tests (repo root) → `scripts/retest.md`
- Scripts conventions → `scripts/best_practices.md`
- Project context → `docs/project-context.md`
- MVP & product checklists (technical / functional / final) → **[Checklists](#smartticket-mvp-checklists) in this README**
- Development log → `docs/dev-log.md`
- Product vision (EN / PT) → `docs/product-vision-en.md`, `docs/product-vision-pt.md`
- Branch delta (`feature/api-mvp` vs `develop`) → `docs/branch-feature-api-mvp-vs-develop.md`
- Team Responsibilities → `docs/team-responsibilities.md`
- Environment template → `.env.example` (never commit `.env`)

---

## 📌 Use Cases

- Customer Support Automation
- IT Incident Classification
- CRM Ticket Routing
- Internal Operations Triage

---

## 💡 Engineering Highlights

- Separation between **training (offline)** and **inference (online)**
- Hybrid AI architecture (ML + LLM)
- Data-driven feedback loop
- API-first design
- Designed for scalability and production use

---

## 🧠 What This Demonstrates

- Data Engineering fundamentals
- Machine Learning lifecycle
- Backend/API development
- System architecture thinking
- AI system design (not just usage)
- Real-world product mindset

---

## 👨‍💻 Authors

**Lucas Marques Maciel**

- 💼 Data & Machine Learning Enthusiast
- 🔗 GitHub: [https://github.com/LucasM-Maciel](https://github.com/LucasM-Maciel)
- 🔗 LinkedIn: [https://www.linkedin.com/in/lucas-marques-maciel](https://www.linkedin.com/in/lucas-marques-maciel)

---

## 📄 License

MIT License
