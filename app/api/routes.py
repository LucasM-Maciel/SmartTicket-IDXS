"""HTTP route handlers (FastAPI).

Implement:

- ``POST /predict`` — body per ``docs/api-contracts.md``; call
  ``predict_category`` from ``app.ml.predict_category``.
- ``POST /health`` — readiness / model artifact checks.

Handlers should validate with ``app.api.schemas`` and stay thin: persistence
belongs in a service layer once the DB exists.
"""
from fastapi import APIRouter

router = APIRouter()

# TODO(Salim): @router.post("/predict") ...
# TODO(Salim): @router.post("/health") ...
