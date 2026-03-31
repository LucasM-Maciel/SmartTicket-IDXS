# Notebooks — Data Exploration & Experiments

## Purpose

This folder is used for:
- Data exploration (EDA)
- Testing preprocessing techniques
- Experimenting with models
- Visualizing results

Notebooks are meant for **experimentation**, not production code.

---

## When to use notebooks

Use notebooks when you need to:
- Understand the dataset
- Test text cleaning strategies
- Try different feature engineering approaches
- Compare model performance
- Visualize data distributions

---

## When NOT to use notebooks

Do NOT:
- Implement production logic here
- Build the final pipeline here
- Depend on notebooks for the system to work

Final logic must always be moved to:
- `app/utils/`
- `app/services/`
- `app/ml/`

---

## Naming Convention

Use ordered names:

```text
01_dataset_exploration.ipynb
02_text_cleaning_tests.ipynb
03_baseline_model.ipynb


Best Practices:
-Keep notebooks clean and readable
-Add explanations for important steps
-Avoid unnecessary code duplication
-Once an experiment is validated → move logic to app/
-Workflow
-Explore in notebook
-Validate idea
-Move final code to app/
-Document decisions in docs/ml-notes.md