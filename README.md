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

**Current endpoint:**

```http
POST /predict
```

Handles:

- Input validation
- Model inference
- Response formatting

---

### 🗃️ Data Layer *(Planned)*

- PostgreSQL (production)
- SQLite (development)

The system is designed to persist structured interaction data for **analytics and continuous improvement**.

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
| Version Control | Git & GitHub |

---

## 📡 API Contract (Current)

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

---

### 🚧 In Progress

- API layer (FastAPI — `POST /predict` endpoint)
- Real-world dataset sourcing (current dataset is synthetic)
- Model evaluation with reliable data

---

### 🔮 Planned

- 🤖 LLM automatic resolution (with structured ML context)
- ⚠️ Dynamic priority + priority aging queue
- 🗃️ Database integration (PostgreSQL)
- 📱 WhatsApp Business API integration (Z-API / Twilio)
- 🖥️ Agent interface (Streamlit demo → React production)
- 🔁 Feedback loop + automatic model retraining
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

## 🛠️ Setup

### 1. Clone

```bash
git clone https://github.com/your-username/intelligent-triage-system.git
cd intelligent-triage-system
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

### 4. Run API

```bash
uvicorn app.main:app --reload
```

---

## 🗺️ Roadmap

### 🔹 MVP

- [x] Preprocessing pipeline
- [x] ML classification model
- [ ] API endpoint

---

### 🔹 Next

- [ ] API versioning
- [ ] Model improvements
- [ ] Modular architecture

---

### 🔹 Future

- [ ] LLM integration
- [ ] Database layer
- [ ] Monitoring & observability
- [ ] Multi-tenant system
- [ ] Cloud deployment

---

## 📄 Documentation

- System Architecture → `docs/architecture.md`
- API Contracts → `docs/api-contracts.md`
- ML Notes → `docs/ml-notes.md`
- Test Plan → `docs/test-plan.md`
- Team Responsibilities → `docs/team-responsibilities.md`

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
