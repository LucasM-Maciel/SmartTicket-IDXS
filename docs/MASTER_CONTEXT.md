<!--
🇧🇷 COMO ATUALIZAR:
- Atualize quando mudar algo importante do projeto
- Esse arquivo é o MAIS usado com o Cursor
-->

# MASTER CONTEXT

## Project

Smart Ticket — Intelligent Ticket Triage System

## Main Flow

```text
Input → API → Pipeline → Classification → Response → Database

MVP
Pipeline working independently
API calling the pipeline
Database persistence
LLM integration (optional initially)
Stack
Python
FastAPI
Pandas
Scikit-learn
SQL
LLM API
Current Decisions
TF-IDF + Logistic Regression
No deep learning
No RAG
Focus on simplicity
Architecture Rules
API handles requests only
Services orchestrate logic
ML handles prediction
Utils handle preprocessing