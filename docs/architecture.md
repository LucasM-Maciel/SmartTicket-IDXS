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
User Input
→ API (FastAPI)
→ Validation
→ Pipeline (clean → normalize → vectorize)
→ ML Model
→ Category + Score
→ Optional LLM Response
→ Save to Database
→ Return Response
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

```
