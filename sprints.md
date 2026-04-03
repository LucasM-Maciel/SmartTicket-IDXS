# 🗺️ Sprint Plan — Intelligent Triage System (Revised)

> Goal: Deliver a functional MVP with ML classification in ~6–8 weeks, with optional LLM and real-world integrations.

---

# ⚪ Sprint 0 — Dataset & Problem Definition

⏱️ **Duration: 3–5 days**

## 🎯 Goal
Define the classification problem and prepare initial dataset

---

### 👨‍💻 Lucas

- [ ] Find or create dataset
- [ ] Analyze data quality
- [ ] Identify noise and inconsistencies
- [ ] Validate dataset usability

---

### 👨‍💻 Rafael

- [ ] Define categories (business + UX perspective)
- [ ] Create examples per category

---

### 🤝 Shared

- [ ] Align classification scope
- [ ] Define initial labels

---

# 🟢 Sprint 1 — Foundation & Setup

⏱️ **Duration: 3–5 days**

## 🎯 Goal
Project structure, environment, and base API running

---

### 👨‍💻 Lucas

- [ ] Create project structure (`app/`, `utils/`, `ml/`, `services/`)
- [ ] Setup initial text cleaning functions
- [ ] Define preprocessing steps

---

### 👨‍💻 Salim

- [ ] Setup FastAPI project
- [ ] Create `main.py`
- [ ] Create `/health` route
- [ ] Define architecture baseline

---

### 👨‍💻 Rafael

- [ ] Improve README overview
- [ ] Create `docs/system-overview.md`

---

### 👨‍💻 Luís

- [ ] Review structure
- [ ] Suggest improvements

---

### 🤝 Shared

- [ ] Align MVP scope

---

# 🟡 Sprint 2 — Data Pipeline & Preprocessing

⏱️ **Duration: 5–7 days**

## 🎯 Goal
Reliable and reusable text preprocessing pipeline

---

### 👨‍💻 Lucas

- [ ] Implement full preprocessing pipeline
- [ ] Token normalization
- [ ] Stopword removal
- [ ] Build reusable utilities

---

### 👨‍💻 Salim

- [ ] Create `services/pipeline.py`
- [ ] Integrate preprocessing into API flow

---

### 👨‍💻 Rafael

- [ ] Create test scenarios
- [ ] Define expected outputs

---

### 👨‍💻 Luís

- [ ] Review preprocessing logic
- [ ] Optimize performance

---

### 🤝 Shared

- [ ] Validate preprocessing quality

---

# 🔵 Sprint 3 — ML Model (Training)

⏱️ **Duration: 4–6 days**

## 🎯 Goal
Train and validate classification model

---

### 👨‍💻 Lucas

- [ ] TF-IDF vectorization
- [ ] Train Logistic Regression
- [ ] Evaluate model (accuracy, precision, recall)
- [ ] Save model artifact (`.pkl`)

---

### 👨‍💻 Rafael

- [ ] Validate categories
- [ ] Create validation examples

---

### 👨‍💻 Luís

- [ ] Review model outputs
- [ ] Suggest improvements

---

### 🤝 Shared

- [ ] Validate model performance

---

# 🔵 Sprint 4 — ML Integration (Inference)

⏱️ **Duration: 4–6 days**

## 🎯 Goal
Integrate trained model into API

---

### 👨‍💻 Lucas

- [ ] Create prediction function
- [ ] Load trained model
- [ ] Ensure preprocessing consistency

---

### 👨‍💻 Salim

- [ ] Integrate ML into `/predict`
- [ ] Define request/response schema

---

### 👨‍💻 Rafael

- [ ] Create API usage examples
- [ ] Document input/output

---

### 👨‍💻 Luís

- [ ] Test integration
- [ ] Debug inconsistencies

---

### 🤝 Shared

- [ ] End-to-end validation (input → prediction → response)

---

# 🟣 Sprint 5 — LLM Integration (Optional)

⏱️ **Duration: 5–7 days**

## 🎯 Goal
Add optional AI-generated responses

---

### 👨‍💻 Lucas

- [ ] Integrate LLM API
- [ ] Pass classification output as context
- [ ] Implement fallback if LLM fails

---

### 👨‍💻 Salim

- [ ] Add LLM into API flow
- [ ] Create toggle (enable/disable LLM)

---

### 👨‍💻 Rafael

- [ ] Design prompt templates per category
- [ ] Define tone and response style

---

### 👨‍💻 Luís

- [ ] Review integration
- [ ] Optimize latency and cost

---

### 🤝 Shared

- [ ] Validate responses quality

---

# 🟠 Sprint 6 — Refinement & Stability

⏱️ **Duration: 6–8 days**

## 🎯 Goal
Stabilize system and improve reliability

---

### 👨‍💻 Lucas

- [ ] Improve model performance
- [ ] Handle edge cases

---

### 👨‍💻 Salim

- [ ] Implement error handling
- [ ] Improve API structure

---

### 👨‍💻 Rafael

- [ ] Final documentation
- [ ] Demo examples

---

### 👨‍💻 Luís

- [ ] Refactor backend
- [ ] Improve maintainability

---

### 🤝 Shared

- [ ] Final testing
- [ ] MVP validation

- [ ] Basic unit tests (pipeline + API)

---

# ⚫ Sprint 7 — Enhancements (Optional)

⏱️ **Duration: 5–7 days**

## 🎯 Goal
Add production-ready improvements

---

- [ ] Logging system
- [ ] Confidence thresholds
- [ ] Basic database integration
- [ ] Monitoring hooks
- [ ] Prepare deployment

---

# 🟤 Sprint 8 — WhatsApp Integration (Business Layer)

⏱️ **Duration: 5–7 days**

## 🎯 Goal
Enable real-world usage via messaging channel

---

### 👨‍💻 Salim

- [ ] Create webhook endpoint
- [ ] Handle incoming messages

---

### 👨‍💻 Lucas

- [ ] Adapt pipeline for real-time messages
- [ ] Ensure inference works with chat input

---

### 👨‍💻 Rafael

- [ ] Define response patterns for chat
- [ ] Improve conversational UX

---

### 👨‍💻 Luís

- [ ] Test integration
- [ ] Debug flow

---

### 🤝 Shared

- [ ] End-to-end validation (WhatsApp → API → Response)

---

# 🧠 Timeline Summary

| Sprint              | Duration |
|-------------------|--------|
| Sprint 0           | 3–5 days |
| Sprint 1           | 3–5 days |
| Sprint 2           | 5–7 days |
| Sprint 3           | 4–6 days |
| Sprint 4           | 4–6 days |
| Sprint 5           | 5–7 days |
| Sprint 6           | 6–8 days |
| Sprint 7 (optional)| 5–7 days |
| Sprint 8 (optional)| 5–7 days |

---

### ⏱️ Total Estimated Time

👉 **~30 a 45 days (MVP)**  

---

# 🧨 Reality Check

- Early sprints → fast progress  
- Mid project → integration complexity  
- Final phase → debugging & refinement  

---

# 🚀 Golden Rule

> If something blocks you for more than 1 day → simplify and move forward

**Delivery > Perfection**
