# Intelligent Triage System

## 🚀 Overview

The Intelligent Triage System is a data-driven application designed to automatically classify and process textual inputs (such as customer messages, tickets, or requests).

The system combines Machine Learning and Large Language Models (LLMs) to transform unstructured text into actionable insights, enabling faster decision-making and improved operational efficiency.

It is built with a modular architecture and aims to be adaptable to different business contexts.

---

## 🧠 Architecture

The system is divided into two main flows:

### 🔵 Online Flow (Real-time)

Input → API → Text Preprocessing → ML Classification → Category/Score → LLM Response (optional) → Database → Output

### 🟢 Offline Flow (Training)

Data Collection → Data Cleaning → Feature Engineering → Model Training → Model Evaluation → Model Persistence

---

## ⚙️ Tech Stack

* **Language:** Python
* **Data Processing:** Pandas
* **Machine Learning:** Scikit-learn (TF-IDF, Logistic Regression)
* **API:** FastAPI
* **Database:** PostgreSQL (or SQLite for development)
* **LLM Integration:** External API (e.g., OpenAI)
* **Version Control:** Git & GitHub

---

## 🔄 Flow

1. The system receives a text input via API
2. The text is cleaned and preprocessed
3. A Machine Learning model classifies the input
4. A category and confidence score are generated
5. (Optional) An LLM generates a contextual response
6. All data is stored in the database
7. The system returns the classification and response

---

## 📊 Features

* Text classification using Machine Learning
* Automated response generation using LLMs
* Data preprocessing pipeline for text normalization
* API for real-time inference
* Logging and storage of inputs, predictions, and outputs
* Modular and scalable architecture

---

## 🛠️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/intelligent-triage-system.git
cd intelligent-triage-system
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

### 5. Test endpoint

Use Postman or browser:

```
POST /predict
```

---

## 📌 Roadmap

### 🔹 Short Term (MVP)

* Implement text preprocessing pipeline
* Train baseline ML model (TF-IDF + Logistic Regression)
* Create API endpoint for classification
* Store results in database

---

### 🔹 Mid Term

* Integrate LLM for automated responses
* Improve model performance and evaluation
* Add logging and monitoring
* Refactor architecture (services, modules)

---

### 🔹 Long Term

* Support multiple use cases (customizable triage)
* Add dashboard or data visualization
* Deploy to cloud environment
* Implement feedback loop for model improvement
* Explore advanced NLP techniques

---

## 💡 Notes

This project is being developed as part of a real-world application with a validation client, focusing on practical impact, scalability, and continuous improvement.
