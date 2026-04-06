
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