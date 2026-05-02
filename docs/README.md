# Documentation index

**Project overview, setup, train/test commands, and roadmap:** see the [root README](../README.md).

## Core references

| Document | Purpose |
|----------|---------|
| `project-context.md` | MVP scope, dev order, future technical planning |
| `branch-feature-api-mvp-vs-develop.md` | API MVP + persistence delta vs older `develop` (historical merge aid) |
| `api-contracts.md` | `GET /health` + `POST /predict` + env (`DATABASE_URL`, `SMARTTICKET_*`, triage) |
| `security-and-deployment.md` | MVP hardening, artifact safety, production run notes |
| *Checklists* | **Technical / functional / final product MVP** — [README (Checklists section)](../README.md#smartticket-mvp-checklists) |
| `architecture.md` | Layers, **`tickets`** schema, **`db/migrations/`** |
| `diagrams/README.md` | Excalidraw: share link + optional `*.excalidraw` in repo (zoom in browser) |
| `adr/` | Architecture decision records (start with `0001-…`) |
| `ml-notes.md` | ML implementation notes and dataset |
| `test-plan.md` | Testing strategy |
| `dev-log.md` | Chronological work log |
| `team-responsibilities.md` | Ownership by person |
| `git-workflow.md` | Branching and collaboration |
| `reuniao-regras-negocio.md` | Business alignment (PT) |
| `product-vision-en.md` / `product-vision-pt.md` | Full product vision |

## Testing & scripts

- Run tests: `scripts/retest.ps1` / `scripts/retest.bat` — details in `scripts/retest.md`
- Manual DB persistence smoke (running API): `scripts/post_test_ticket.py`
- Environment template (repo root): `/.env.example` — copy to `.env`, never commit secrets
- Test tips: `tests/best_practices.md`
- Script conventions: `scripts/best_practices.md`

## Naming & editor

- `naming-conventions.md`
- `cursor-rules.md`
