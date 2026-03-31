
# Scripts — Operational & Utility Tasks

## Purpose

This folder contains scripts used to:
- Run training processes
- Preprocess datasets
- Execute batch operations
- Perform one-time or repeatable tasks

Scripts are **entry points for tasks**, not core logic.

---

## When to use scripts

Use scripts when you need to:
- Train the model from terminal
- Prepare or transform datasets
- Run data pipelines manually
- Execute maintenance tasks

---

## Examples

```text
run_training.py
preprocess_dataset.py
generate_predictions.py


Example Usage

python scripts/run_training.py

Important Rule

Scripts should:

Call logic from app/
NOT contain business logic themselves

Example:

from app.ml.train import train_model

if __name__ == "__main__":
    train_model()

    Do NOT
-Duplicate logic already inside app/
-Write full pipelines here
-Mix experimentation code (use notebooks instead)
-Best Practices
-Keep scripts simple and focused
-Use them as wrappers for real logic
-Clearly name scripts based on their purpos