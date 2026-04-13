# Notebooks — data exploration & experiments

## Purpose

This folder is for:

- Data exploration (EDA)
- Testing preprocessing ideas
- Model experiments
- Visualizations

Notebooks are for **experimentation**, not production code.

## When to use notebooks

- Understand the dataset
- Try cleaning / normalization variants
- Compare models or features
- Plot distributions

## When not to use notebooks

Do **not** put production logic only in notebooks. Move validated code to:

- `app/utils/`
- `app/services/`
- `app/ml/`

## Naming

```text
01_dataset_exploration.ipynb
02_text_cleaning_tests.ipynb
03_baseline_model.ipynb
```

## Practices

- Keep notebooks readable; explain non-obvious steps
- After an experiment wins → port to `app/` and note decisions in `docs/ml-notes.md`
