````md
# Project Context

## Product
Smart Ticket — Intelligent Ticket Triage System

---

## Problem
Companies receive a large volume of unstructured customer messages and struggle to:
- Classify requests  
- Prioritize tickets  
- Respond efficiently  

---

## Solution
Automate ticket triage using:
- Machine Learning (classification)  
- LLM (response generation)  
- API (integration)  
- SQL (storage)  

---

## Main Flow

```text
Input → API → Pipeline → Classification → Response → Database
````

---

## MVP Definition

The MVP includes:

* Pipeline working independently
* API calling the pipeline
* Database persistence
* Basic response generation (LLM optional at first)

---

## Key Decisions

* Use TF-IDF + Logistic Regression (baseline)
* No deep learning for MVP
* No RAG for MVP
* Focus on simplicity and fast delivery

---

## Development Order

1. Data processing (Pandas, cleaning)
2. ML classification
3. API integration
4. SQL persistence
5. LLM integration
6. Deployment

```