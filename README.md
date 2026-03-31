# 🧠 Intelligent Triage System

> End-to-end intelligent system for classifying and processing customer tickets using Machine Learning and (optionally) LLMs.

<p align="center">
  <b>Designed with real-world architecture principles • Scalable • Modular • Production-oriented</b>
</p>

---

## 🚀 Overview

The **Intelligent Triage System** is a production-oriented application designed to process and understand unstructured text data such as support tickets, user requests, and operational messages.

It combines:

- 🧠 **Machine Learning** → structured classification  
- 🤖 **LLMs (planned)** → contextual and human-like responses  
- ⚙️ **Data Pipelines** → robust preprocessing and transformation  

---

### 🎯 Goal

Transform raw text into:

- 📌 Category (intent)  
- 📊 Confidence score  
- ⚠️ *(Future)* Priority (urgency)  
- 💬 *(Future)* Automated response  

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
(Optional) LLM Response
↓
(Optional) Database Persistence
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

````

---

## 🧩 Core Components

### 📦 Data Pipeline

- Text normalization  
- Stop-word removal  
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

- Context-aware response generation  
- Prompt conditioning based on classification output  

Future possibilities:
- Chat automation  
- Knowledge base integration  

---

### 🌐 API Layer

- Built with **FastAPI**
- RESTful architecture (initial version simplified)

**Current endpoint:**
```http
POST /predict
````

Handles:

* Input validation
* Model inference
* Response formatting

---

### 🗃️ Data Layer *(Planned)*

* PostgreSQL (production)
* SQLite (development)

Planned storage:

* Input text
* Predictions
* Metadata
* Logs

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

- 🤖 LLM response generation  
- ⚠️ Priority classification  
- 🗃️ Database integration  
- 📈 Logging & monitoring  
- ☁️ Cloud deployment  
- 📱 WhatsApp integration (webhooks & messaging APIs)
  - Receive messages via webhook  
  - Automatic ticket creation from conversations  
  - Real-time classification of incoming messages  
  - Automated responses via WhatsApp Business API  

---

## 📈 Model Evaluation

> Metrics will be added after training validation pipeline is finalized.

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
* Clean ML pipeline design
* API-first architecture
* Designed for future scalability

---

## 🧠 What This Demonstrates

* Data Engineering fundamentals
* Machine Learning lifecycle
* Backend/API design
* System architecture thinking
* AI + Software Engineering integration

---

## 👨‍💻 Authors

**Lucas Marques Maciel**

* 💼 Data & Machine Learning Enthusiast
* 🔗 GitHub: [https://github.com/LucasM-Maciel](https://github.com/LucasM-Maciel)
* 🔗 LinkedIn: [https://www.linkedin.com/in/lucas-marques-maciel](https://www.linkedin.com/in/lucas-marques-maciel)

---

## 📄 License

MIT License

```



