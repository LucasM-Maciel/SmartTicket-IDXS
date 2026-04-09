
<!--
🇧🇷 COMO ATUALIZAR:
- Atualize TODO DIA que trabalhar
- Seja simples: o que fez, problema, solução
- Isso mostra evolução real
-->

# Development Log

## 2026-03-31 (Lucas)

### What was done
- Project structure created
- Documentation structure created
- Defined MVP scope
- Defined pipeline architecture

### Problems
- Understanding architecture layers
- Organizing responsibilities

### Solutions
- Defined layered architecture
- Created documentation for context

### Learnings
- Pipeline must be validated before API
- Separation of concerns is critical

### Next Steps
- Implement clean_text
- Implement normalize_text
- Build first pipeline version

---

## 2026-04-06 (Lucas)

### What was done
- Created skeleton of `app/utils/text_cleaning.py`
- Implemented `clean_text` function: lowercase, strip, remove symbols via regex, normalize whitespace
- Implemented `normalize_text` in `app/utils/normalizer.py`: removes stopwords via NLTK with configurable language parameter

### Problems
- `clean_text`: function would fail if input was not a string (e.g. NaN, None from the dataset)
- `normalize_text`: challenge was keeping the code clean and readable while handling edge cases properly

### Solutions
- Non-string inputs return empty string in both functions — safe for the pipeline and avoids constant exceptions
- `LookupError` caught on NLTK corpus load: prints download instructions and returns empty string gracefully

### Learnings
- Regex is more powerful than expected — learned new patterns during implementation
- Learned more about string manipulation in Python
- Defensive input handling is better than error propagation in pipeline contexts

### Next Steps
- Implement `pipeline.py` connecting `clean_text` → `normalize_text` → vectorizer → model

---

## 2026-04-07 (Lucas)

### What was done
- Implemented `app/services/pipeline.py`: `run_pipeline` connects `clean_text` → `normalize_text`
- Implemented `app/ml/train.py`: loads dataset, applies pipeline, trains TF-IDF + Logistic Regression, saves model and vectorizer artifacts via `joblib`
- Implemented `app/ml/predict.py`: loads saved artifacts and returns predicted category + confidence score for a given text
- Ran first model training against `customer_support_tickets.csv`
- Updated `run_pipeline` in `app/services/pipeline.py` to accept a `language` parameter (default: `"english"`), enabling future Portuguese support
- Created `docs/product-vision-pt.md` and `docs/product-vision-en.md`: complete product vision defining system flow, LLM layer, priority logic, human queue, agent interface, database structure, business model and deployment strategy
- Updated `docs/project-context.md`: expanded with full product definition, key decisions, complete development order with status, and timeline
- Updated `docs/ml-notes.md`: added confidence threshold, multi-message classification strategy (Approach A/B), and feedback loop
- Updated `docs/architecture.md`: expanded online flow, added database structure and full tech stack
- Updated `README.md`: updated system architecture, tech stack, and planned features to reflect full product vision

### Problems
- Dataset is synthetic: ticket descriptions have no clear semantic relationship with the labels, making it impossible to assess real model accuracy
- `predict.py` depends on artifacts existing — if `train.py` hasn't run yet, it would crash at import time

### Solutions
- `FileNotFoundError` caught at module load in `predict.py`: exits with a clear message instructing the user to run `train.py` first
- Dataset issue flagged for replacement — current results are not representative of real-world performance

### Learnings
- Learned the basics of TF-IDF vectorization and Logistic Regression in Scikit-learn
- Synthetic datasets can produce misleading metrics — data quality is critical before trusting any model evaluation
- Multilingual support requires separate models per language — a single model cannot handle both English and Portuguese reliably

### Next Steps
- Find a better (real) dataset to replace `customer_support_tickets.csv`
- Find a Portuguese dataset and train a separate Portuguese model to enable multilingual support