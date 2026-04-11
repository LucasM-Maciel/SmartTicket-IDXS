````md id="sysarch001"
# System Architecture

## Overview

The system follows a layered architecture:

- API Layer → handles HTTP requests  
- Service Layer → orchestrates logic  
- ML Layer → handles predictions  
- Utils Layer → text processing  
- Data Layer → datasets and storage  

---

## Online Flow (Production)

```text
Customer sends message on WhatsApp
→ WhatsApp Business API (Z-API / Twilio) → webhook
→ FastAPI: validate + save contact/ticket to database
→ Pipeline (clean → normalize → vectorize)
→ ML Model: category + confidence score
→ Score ≥ 0.75?
    Yes → LLM attempts automatic resolution
            → Customer confirms resolution?
                Yes → close ticket as resolved
                No  → escalate to human queue
    No  → goes directly to human queue (low confidence flag)
→ Human queue ordered by dynamic priority (priority aging)
→ Agent responds via SmartTicket interface
→ System sends response via WhatsApp API
→ Everything stored in database → analytics + retraining
````

---

## Offline Flow (Training)

```text
Dataset
→ Cleaning
→ Feature Engineering
→ Train Model
→ Evaluate
→ Save Model
```

---

## Folder Responsibilities

* `app/api` → routes and request handling
* `app/services` → pipeline orchestration
* `app/ml` → training and prediction
* `app/utils` → reusable functions
* `app/data` → datasets
* `app/core` → configs
* `scripts/` → thin CLI wrappers (e.g. pytest from repo root); must call logic in `app/`, not duplicate it

---

## Database Structure (Planned)

* **CONTACTS** — whatsapp_number, name, is_customer, became_customer_at
* **TICKETS** — text, text_processed, category, score, priority, priority_score, status, assigned_to, resolved_by
* **MESSAGES** — ticket_id, direction (inbound/outbound), sent_by (llm/human/system)
* **FEEDBACK** — ticket_id, correct_category, was_classification_correct, agent_id
* **CONVERSIONS** — contact_id, ticket_id, converted_at

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend / API | Python + FastAPI |
| ML | Scikit-learn (TF-IDF + Logistic Regression) |
| LLM | OpenAI API *(planned)* |
| Database | PostgreSQL — Supabase (MVP), Railway/RDS (production) |
| WhatsApp | Z-API (Brazil) or Twilio *(planned)* |
| Real-time | WebSockets via FastAPI — polling for demo |
| Agent interface | Streamlit (demo) → React / Next.js (production) |
| Scheduled jobs | APScheduler (priority aging + retraining) |
| Data processing | Pandas |
