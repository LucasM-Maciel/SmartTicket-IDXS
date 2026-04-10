# Smart Ticket — Intelligent Ticket Triage System

## Overview
Smart Ticket is an intelligent ticket triage system that uses Machine Learning and LLMs to classify and respond to customer messages.

## Objective
Receive unstructured text (customer messages) and:
- classify the request (ML)
- generate a response (LLM)
- store data (SQL)
- expose functionality via API

## Tech Stack
- Python
- FastAPI
- Pandas
- Scikit-learn
- SQL
- LLM API

## Testing

- Test strategy and priorities: `docs/test-plan.md`
- Implementations: `tests/`

## Architecture (High-Level)

```text
Input → API → Pipeline → ML → LLM → Database → Output