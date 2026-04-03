# 🧠 Intelligent Triage System

> End-to-end intelligent system for classifying, processing, and learning from customer tickets using Machine Learning and LLMs.

<p align="center">
  <b>Built with real-world architecture principles • Scalable • Modular • Production-oriented</b>
</p>

---

## 🚀 Overview

The **Intelligent Triage System** is a production-oriented application designed to process and understand unstructured text data such as support tickets, user requests, and operational messages.

It combines:

* 🧠 **Machine Learning** → structured classification
* 🤖 **LLMs (planned)** → contextual and human-like responses
* ⚙️ **Data Pipelines** → robust preprocessing and transformation
* 📊 **Data Layer** → analytics, monitoring, and continuous improvement

---

### 🎯 Goal

Transform raw text into:

* 📌 Category (intent)
* 📊 Confidence score
* ⚠️ *(Future)* Priority (urgency)
* 💬 *(Future)* Automated response

While also enabling:

* 📈 Business insights
* 🔁 Continuous learning
* ⚙️ Operational optimization

---

## 🏗️ System Architecture

### 🔵 Online Flow (Real-Time Inference)

```
Client
↓
API (FastAPI)
↓
Text Preprocessing Pipeline
↓
Feature Extraction (TF-IDF)
↓
ML Model (Logistic Regression)
↓
Classification (Category + Score)
↓
LLM (Context-Aware Response) [Optional]
↓
Database Persistence (Analytics & Learning)
↓
API Response
```

---

### 🟢 Offline Flow (Training Pipeline)

```
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

* Text normalization
* Stop-word removal
* Token standardization
* Noise reduction (punctuation, casing, etc.)

---

### 🧠 Machine Learning Layer

* **Vectorization:** TF-IDF
* **Model:** Logistic Regression

**Current Output:**

* Category classification
* Confidence score

**Planned:**

* Priority classification (multi-output or secondary model)

---

### 🤖 LLM Layer *(Planned)*

The LLM layer is designed to operate with **structured context from the ML model**, not as a standalone black box.

Instead of relying only on raw input, the LLM receives:

* Predicted category
* Confidence score
* *(Future)* Priority level

This hybrid approach ensures:

* Higher response accuracy
* Reduced hallucination risk
* More controlled and consistent outputs
* Better alignment with business logic

#### Example Flow:

```
User message
→ ML classification
→ Context injection (category + score)
→ LLM response generation
```

---

### 🌐 API Layer

* Built with **FastAPI**
* RESTful architecture (initial version simplified)

**Current endpoint:**

```http
POST /predict
```

Handles:

* Input validation
* Model inference
* Response formatting

---

### 🗃️ Data Layer *(Planned)*

* PostgreSQL (production)
* SQLite (development)

The system is designed to persist structured interaction data for **analytics and continuous improvement**.

---

## 📊 Data & Analytics Layer

The system is not only designed for real-time inference but also for **data collection and intelligence generation**.

Each interaction can store:

* Raw input text
* Processed text
* Predicted category
* Confidence score
* *(Future)* Priority
* LLM-generated response
* Timestamps and metadata
* *(Future)* Human-validated outcomes

---

### 🎯 Purpose

This enables:

* 📈 Business analytics

  * Most frequent issues
  * Demand peaks
  * Category distribution

* 🧠 Continuous model improvement

  * Retraining with real-world data
  * Error correction

* 🔍 Model evaluation and auditing

* ⚙️ Operational insights

  * Support team optimization
  * SLA improvements

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

| Category        | Technology                      |
| --------------- | ------------------------------- |
| Language        | Python                          |
| Data Processing | Pandas                          |
| ML              | Scikit-learn                    |
| API             | FastAPI                         |
| Database        | PostgreSQL / SQLite *(planned)* |
| LLM             | OpenAI API *(planned)*          |
| Version Control | Git & GitHub                    |

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

* 🧠 ML-based text classification
* ⚡ FastAPI inference endpoint
* 🔄 Text preprocessing pipeline

---

### 🚧 In Progress

* API structuring (versioning, routes)
* Improved preprocessing
* Model tuning

---

### 🔮 Planned

* 🤖 LLM response generation
* ⚠️ Priority classification
* 🗃️ Database integration
* 📈 Logging & monitoring
* ☁️ Cloud deployment
* 📱 WhatsApp integration (webhooks & messaging APIs)

---

## 📈 Model Evaluation

> Metrics will be added after validation pipeline is finalized.

Planned metrics:

* Accuracy
* Precision / Recall / F1-score
* Confusion matrix
* Business-oriented metrics (resolution success, response time)

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

* [ ] Preprocessing pipeline
* [ ] ML classification model
* [ ] API endpoint

---

### 🔹 Next

* [ ] API versioning
* [ ] Model improvements
* [ ] Modular architecture

---

### 🔹 Future

* [ ] LLM integration
* [ ] Database layer
* [ ] Monitoring & observability
* [ ] Multi-tenant system
* [ ] Cloud deployment

---

## 📌 Use Cases

* Customer Support Automation
* IT Incident Classification
* CRM Ticket Routing
* Internal Operations Triage

---

## 💡 Engineering Highlights

* Separation between **training (offline)** and **inference (online)**
* Hybrid AI architecture (ML + LLM)
* Data-driven feedback loop
* API-first design
* Designed for scalability and production use

---

## 🧠 What This Demonstrates

* Data Engineering fundamentals
* Machine Learning lifecycle
* Backend/API development
* System architecture thinking
* AI system design (not just usage)
* Real-world product mindset

---

## 👨‍💻 Authors

**Lucas Marques Maciel**

* 💼 Data & Machine Learning Enthusiast
* 🔗 GitHub: [https://github.com/LucasM-Maciel](https://github.com/LucasM-Maciel)
* 🔗 LinkedIn: [https://www.linkedin.com/in/lucas-marques-maciel](https://www.linkedin.com/in/lucas-marques-maciel)

---

## 📄 License

MIT License

---

