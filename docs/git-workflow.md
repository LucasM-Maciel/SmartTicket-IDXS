# 🔀 Git Workflow — Intelligent Triage System

## 🎯 Purpose

This document defines how the team collaborates using Git.

The goal is to ensure:

- clean commit history
- safe integrations
- clear ownership of changes
- scalable collaboration

---

# 🧠 Core Principles

- Never break `main`
- Always work in isolated branches
- Keep PRs small and focused
- Prefer clarity over speed
- Review before merging

---

# 🌿 Branch Strategy

## Main branches

```text
main     → stable / production-ready
develop  → integration branch (team work)
```

**Docs:** Evolve `docs/architecture.md` and `docs/adr/` on **`develop`** (via `docs/*` or feature branches), then merge to **`main`** on release so the stable branch does not accumulate narrative-only drift.

---

## Working branches

```text
feature/*
fix/*
docs/*
test/*
refactor/*
```

---

## Examples

```text
feature/text-preprocessing
feature/predict-endpoint
feature/llm-integration
fix/api-validation
docs/readme-update
test/pipeline-tests
refactor/service-layer
```

---

# 🔁 Development Flow

## Step 1 — Update local repository

```bash
git checkout develop
git pull origin develop
```

---

## Step 2 — Create your branch

```bash
git checkout -b feature/your-feature-name
```

---

## Step 3 — Work and commit

```bash
git add .
git commit -m "feat: add text preprocessing pipeline"
```

---

## Step 4 — Push your branch

```bash
git push origin feature/your-feature-name
```

---

## Step 5 — Open Pull Request (PR)

```text
feature/your-feature-name → develop
```

---

## Step 6 — Code Review

Before merging, ensure:

- code follows naming conventions
- no duplicated logic (DRY)
- responsibilities are well separated
- no debug code left
- tests (if applicable) are passing

---

## Step 7 — Merge into develop

- After approval
- Resolve conflicts if needed
- Keep history clean

---

## Step 8 — Release to main

When `develop` is stable:

```text
develop → main
```

---

# 📌 Rules

## 🚫 Never

- commit directly to `main`
- commit directly to `develop` (always use PR)
- work on someone else's branch
- create generic branches (`lucas-branch`)
- open PRs with multiple unrelated changes

---

## ✅ Always

- create one branch per task
- use descriptive names
- keep commits small and meaningful
- pull latest `develop` before starting work
- resolve conflicts early

---

# 🧾 Commit Convention

We use **Conventional Commits**:

```text
feat: new feature
fix: bug fix
docs: documentation
refactor: code improvement
test: tests
chore: maintenance
```

---

## Examples

```text
feat: add preprocessing pipeline
fix: correct predict response schema
docs: update API contracts
refactor: simplify prediction service
test: add preprocessing tests
```

---

# 🧪 Pull Request (PR) Guidelines

## Title

```text
[feature] add preprocessing pipeline
```

---

## Description Template

```md
## What was done
- Implemented text preprocessing
- Added normalization and cleaning

## Why
- Required for ML pipeline

## How to test
- Run API
- Send sample request

## Checklist
- [ ] Code follows naming conventions
- [ ] No duplicated logic
- [ ] No debug code
- [ ] Tests added (if needed)
```

---

# 🔄 Keeping Branch Updated

Before opening PR:

```bash
git checkout develop
git pull
git checkout feature/your-branch
git merge develop
```

---

# ⚔️ Handling Conflicts

- Resolve locally
- Test after resolving
- Never ignore conflicts

---

# 🧠 Best Practices

- One responsibility per PR
- Prefer multiple small PRs over one large PR
- Write self-explanatory code
- Review your own code before requesting review

---

# 🚀 Recommended Team Usage

## Lucas (ML / Data)

```text
feature/preprocessing
feature/model-training
feature/pipeline
```

---

## Salim (Backend)

```text
feature/api-structure
feature/routes
feature/database
```

---

## Rafael (Docs / UX / LLM)

```text
docs/readme
docs/api-contracts
feature/prompts
```

---

## Luís (Tests / Refactor)

```text
test/pipeline
test/api
refactor/services
```

---

# 🧠 Workflow Summary

```text
develop
  ↑
feature/*
  ↓
PR → develop
  ↓
stable → merge → main
```

---

# 📌 Final Rule

> If your change breaks the system or is unclear, it should not be merged.

---

# 🎯 Goal

This workflow ensures that:

- the system remains stable
- collaboration is efficient
- the codebase scales cleanly
- every change is traceable

---

> Good Git workflow = faster development + fewer bugs + better collaboration