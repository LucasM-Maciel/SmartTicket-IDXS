# Team Responsibilities

> **What is in the repo today:** The **current technical MVP** (preprocessing, ML, `app/api` on `feature/api-mvp`, `app/core`, `app/main.py`, tests, and the documentation that tracks it) is **solely Lucas’s work**. The sections below split **intended** ownership for **upcoming** work (persistence, broader backend, docs/UX support, reviews) — they do **not** mean those people have contributed code or docs to the MVP that is being merged now.

---

## Lucas (Data, ML & Core Backend)

### Main Responsibilities
- Data pipeline
- Text cleaning and normalization
- Feature engineering
- Text classification logic
- ML model training
- Model evaluation
- Model loading and prediction
- LLM integration logic
- Core inference pipeline (ML → API integration)
- Business logic for ticket processing
- Analytical decisions related to ticket triage

### Main Files / Areas
- `app/utils/`
- `app/ml/`
- `app/services/pipeline.py`
- `app/api/` (routes, schemas — **implemented by Lucas** for the technical API MVP)
- `app/core/` (config, limits — **implemented by Lucas**)
- `app/main.py` (**implemented by Lucas**)
- ML-related and API-contract documentation (`docs/ml-notes.md`, `docs/api-contracts.md`, etc.)

---

## Salim (Tech Lead & Backend) — *no code in the current technical MVP*

### Main Responsibilities
- FastAPI application structure
- Route creation and organization
- Request/response handling
- Schema definition and validation
- Backend architecture design
- Database integration (planned)
- System design decisions
- Ensuring integration between ML, API, and future components
- Sprint planning and technical prioritization

### Main Files / Areas (target — *no MVP code from Salim to date*)
- `app/api/` (future: larger route surface, service layer with DB)
- `app/core/`
- `app/main.py` (future: CORS, lifespan, middleware)
- Architecture decisions
- Backend structure and standards

---

## Rafael (Documentation, UX & Support) — *not yet a contributor to the technical MVP*

### Main Responsibilities
- Documentation (README, docs, usage guides)
- Functional descriptions of features
- Prompt engineering support for LLM
- Response templates and tone definition
- UX of text interactions
- Writing system usage examples
- Creating test scenarios
- Supporting definition of categories and responses

### Main Files / Areas
- `docs/`
- prompt drafts
- response templates
- test scenarios
- usage examples

---

## Luís (Backend Support - Weekend Contributor) — *not yet a contributor to the technical MVP*

### Main Responsibilities
- Backend code review
- Refactoring and code quality improvements
- Debugging support for complex issues
- Assisting in architectural improvements
- Supporting API optimization and organization

### Main Files / Areas
- Backend modules (review & refactor)
- `app/api/`
- `app/core/`
- General backend improvements

---

## Shared Responsibilities

These responsibilities involve more than one team member (for **future** alignment — they are **not** shared deliverables on the current technical MVP, which is single-author):

- Defining ticket categories
- Reviewing architecture decisions
- Aligning API contracts
- Reviewing MVP scope
- Integration testing
- Final delivery validation
- Dataset understanding and refinement
