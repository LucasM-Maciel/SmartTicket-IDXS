<!--
🇧🇷 COMO ATUALIZAR:
- Atualize este documento sempre que o time adotar novos padrões
- Este arquivo deve ser a fonte única de verdade sobre naming e organização
-->

# 🧩 Naming Conventions & Code Standards

## 🎯 Purpose

This document defines the naming conventions, code organization rules, and development principles used in the **Intelligent Triage System**.

The goal is to ensure:

- consistency across the codebase
- readability and maintainability
- scalable architecture
- efficient team collaboration

---

# 🧠 Core Principles

We follow these principles:

- **Clarity over cleverness**
- **Consistency over personal preference**
- **Simplicity over unnecessary abstraction**
- **Reusability without overengineering**
- **Explicit is better than implicit**

---

# 🔤 1. Naming Conventions

## 1.1 Variables

### Rule
Use **snake_case**

### Examples

```python
ticket_text = "cancel my order"
cleaned_text = preprocess_text(ticket_text)
confidence_score = 0.92
```

### Avoid

```python
ticketText = "..."
x = "..."
dataFinalProcessed = "..."
```

---

## 1.2 Constants

### Rule
Use **UPPER_SNAKE_CASE**

```python
MODEL_PATH = "artifacts/model.pkl"
MIN_CONFIDENCE = 0.75
SUPPORTED_CHANNELS = ["api", "whatsapp"]
```

---

## 1.3 Functions

### Rule
Use **snake_case + verb-based naming**

```python
def clean_text(text: str) -> str:
    ...

def predict_category(text: str) -> dict:
    ...

def load_model(path: str):
    ...
```

### Avoid vague names

```python
def process():
def handle():
def do_it():
```

---

## 1.4 Classes

### Rule
Use **PascalCase**

```python
class TextPreprocessor:
class PredictionService:
class LLMService:
class PredictRequest:
```

---

## 1.5 Boolean Variables

### Rule
Must read like a true/false statement

```python
is_valid_text = True
has_low_confidence = False
is_llm_enabled = True
```

---

## 1.6 Collections

### Rule
Use plural names

```python
categories = ["billing", "support"]
predictions = []
metrics = {"accuracy": 0.91}
```

---

# 📁 2. File Naming

### Rule
Use **snake_case**

### Examples

```text
text_cleaning.py
prediction_service.py
pipeline.py
api_schemas.py
```

---

# 🗂️ 3. Folder Structure

```text
app/
├── api/
├── services/
├── ml/
├── utils/
├── core/
├── data/
├── artifacts/
├── tests/
└── docs/
```

---

## Folder Responsibilities

### `api/`
- routes
- request/response schemas

### `services/`
- orchestration logic
- pipeline coordination

### `ml/`
- training
- prediction logic
- model loading

### `utils/`
- reusable helpers
- text processing

### `core/`
- configs
- constants

---

# 🌐 4. API Naming

### Current (MVP)

```http
POST /predict
GET /health
```

### Future

```http
POST /api/v1/tickets/analyze
```

---

# 🧾 5. Schema Naming

Use **PascalCase**

```python
class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    category: str
    score: float
```

---

# 📦 6. Model & Artifacts Naming

```text
model_v1.pkl
tfidf_vectorizer_v1.pkl
metrics_v1.json
```

---

# 🌿 7. Branch Naming

```text
feature/preprocessing
feature/model-training
fix/predict-endpoint
docs/update-readme
```

---

# 💬 8. Commit Naming

```text
feat: add preprocessing pipeline
fix: correct prediction output
docs: update API contracts
refactor: simplify pipeline logic
test: add preprocessing tests
```

---

# 🔁 9. DRY Principle

## Definition

**DRY = Don’t Repeat Yourself**

---

## How we apply DRY

### ✅ Single source of truth

Preprocessing logic must exist in only one place:

```text
app/utils/text_cleaning.py
```

Used by:
- training
- inference
- tests

---

### ❌ Avoid duplication

Do NOT:

- rewrite cleaning logic in notebooks
- duplicate logic in API routes
- create multiple versions of same function

---

### ✅ Use services

Correct:

```python
result = prediction_service.predict(text)
```

Wrong:

```python
# inside route
clean text
vectorize
predict
```

---

### ✅ Centralize constants

```python
MIN_CONFIDENCE = 0.75
```

---

# 🧼 10. Clean Code Principles

## 10.1 Single Responsibility

```python
def clean_text():
def predict():
```

❌ Avoid:

```python
def clean_train_predict_save():
```

---

## 10.2 Small functions

Break logic into steps:

```python
clean_text()
vectorize_text()
predict()
format_response()
```

---

## 10.3 Meaningful names

```python
confidence_score
prediction_result
```

❌ Avoid:

```python
x
data2
result_final_abc
```

---

## 10.4 Clear layer separation

| Layer | Responsibility |
|------|--------------|
| API | HTTP handling |
| Services | orchestration |
| ML | prediction |
| Utils | helpers |

---

## 10.5 Avoid premature abstraction

Start simple → abstract later

---

## 10.6 Comments = WHY, not WHAT

```python
# fallback when confidence is too low
```

---

## 10.7 Notebooks are NOT production

Notebooks are for:
- experimentation
- EDA

Production code goes to:

```text
app/utils/
app/services/
app/ml/
```

---

## 10.8 Make flow obvious

```python
cleaned = clean_text(text)
features = vectorize(cleaned)
prediction = predict(features)
```

---

# 🧠 11. Team Rules

## Always

- use consistent naming
- reuse existing logic
- keep layers separated
- refactor duplicated code
- write readable code

---

## Never

- duplicate preprocessing logic
- put ML logic inside API routes
- rely on notebooks for production
- use unclear names
- leave temporary code

---

# 🚀 12. System Flow (Reference)

```text
Request
→ API
→ Service
→ Preprocessing
→ ML
→ (Optional LLM)
→ Response
```

---

# 🧠 Final Rule

Before writing code, ask:

1. Is the name clear?
2. Am I duplicating logic?
3. Does this belong in this layer?
4. Can someone else understand this fast?
5. Will this make sense in 30 days?

If not → simplify.

---

# 📌 Summary

This project follows:

- snake_case → variables, functions, files  
- PascalCase → classes, schemas  
- UPPER_SNAKE_CASE → constants  
- DRY → no duplicated logic  
- Clean Code → readable, modular, maintainable  

---

> The goal is not just to make the system work — but to make it understandable, scalable, and reliable.