
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

### Problems
- Function would fail if input was not a string (e.g. NaN, None from the dataset)

### Solutions
- Added type check at the start of the function: non-string inputs return an empty string instead of raising an error
- Empty string is safe for the ML pipeline and avoids constant exceptions during model feeding

### Learnings
- Regex is more powerful than expected — learned new patterns during implementation
- Defensive input handling is better than error propagation in pipeline contexts

### Next Steps
- Implement `normalize_text` (in progress today)
- `normalize_text` is still part of the clean stage of the pipeline