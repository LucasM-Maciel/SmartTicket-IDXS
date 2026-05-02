"""FastAPI application entry point.

Implement: lifespan, CORS, global exception handlers as needed. Routers live in
``app.api.routes`` — keep this file limited to app assembly.

Do **not** put ML or preprocessing here; routes should call a thin service
(e.g. ``classify_ticket``), not heavy pipeline code.
"""
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="SmartTicket-IDXS", version="0.1.0")
app.include_router(router)
