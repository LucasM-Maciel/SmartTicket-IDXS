<!--
🇧🇷 COMO ATUALIZAR:
- Atualize se perceber erros recorrentes do Cursor
- Adicione regras novas conforme o projeto evolui
-->

# Cursor Rules

## General Rules

- Follow layered architecture
- Keep code simple (MVP focus)
- Avoid unnecessary abstractions

## Architecture Rules

- API must not contain business logic
- API calls services
- Services orchestrate the pipeline
- ML handles prediction only
- Utils contain reusable functions

## ML Rules

- Use TF-IDF + Logistic Regression (baseline)
- Do not use deep learning for now
- Keep pipeline deterministic

## Development Rules

- Explain logic before implementing
- Prefer simple solutions
- Avoid overengineering

## Context Priority

Always prioritize:

- project-context.md
- architecture.md
- api-contracts.md
- scripts/best_practices.md (when adding or changing `scripts/`)
- scripts/retest.md (when changing test runner wrappers)