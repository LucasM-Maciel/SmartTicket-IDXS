<!--
🇧🇷 COMO ATUALIZAR:
- Atualize sempre que o escopo mudar
- Se mudarem tecnologias (ex: trocar modelo), registre aqui
- Se o MVP mudar, atualize a seção "MVP Definition"
-->

# Project Context

## Product
Smart Ticket — Intelligent Ticket Triage System

## Problem
Companies receive a large volume of unstructured customer messages and struggle to:
- classify requests
- prioritize tickets
- respond efficiently

## Solution
Automate ticket triage using:
- Machine Learning (classification)
- LLM (response generation)
- API (integration)
- SQL (storage)

## Main Flow

```text
Input → API → Pipeline → Classification → Response → Database

MVP Definition

The MVP includes:

-Pipeline working independently
-API calling the pipeline
-Database persistence
-Basic response generation (LLM optional at first)
-Key Decisions
-Use TF-IDF + Logistic Regression (baseline)
-No deep learning for MVP
-No RAG for MVP
-Focus on simplicity and fast delivery
-Development Order
-Data processing (Pandas, cleaning)
-ML classification
-API integration
-SQL persistence
-LLM integration
-Deployment