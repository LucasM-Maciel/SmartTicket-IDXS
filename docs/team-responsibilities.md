# Team Responsibilities

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
- ML integration inside API routes
- `docs/ml-notes.md`

---

## Salim (Tech Lead & Backend)

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

### Main Files / Areas
- `app/api/`
- `app/core/`
- `app/main.py`
- Architecture decisions
- Backend structure and standards

---

## Rafael (Documentation, UX & Support)

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

## Luís (Backend Support - Weekend Contributor)

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

These responsibilities involve more than one team member:

- Defining ticket categories
- Reviewing architecture decisions
- Aligning API contracts
- Reviewing MVP scope
- Integration testing
- Final delivery validation
- Dataset understanding and refinement
