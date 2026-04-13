"""FastAPI application entry point.

Implement: lifespan, CORS, global exception handlers as needed. Routers live in
``app.api.routes`` — keep this file limited to app assembly.

Do **not** put ML or preprocessing here; call ``predict_category`` only from
route handlers (or a thin service).
"""
from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="SmartTicket-IDXS", version="0.1.0")
app.include_router(router)
