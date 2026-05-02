"""FastAPI application entry point.

Implement: lifespan, CORS, global exception handlers as needed. Routers live in
``app.api.routes`` — keep this file limited to app assembly.

Do **not** put ML or preprocessing here; routes should call a thin service
(e.g. ``classify_ticket``), not heavy pipeline code.
"""
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import fastapi_documentation_kwargs
from app.core.nltk_bootstrap import ensure_nltk_stopwords


@asynccontextmanager
async def lifespan(_: FastAPI):
    ensure_nltk_stopwords()
    yield


app = FastAPI(
    title="SmartTicket-IDXS",
    version="0.1.0",
    lifespan=lifespan,
    **fastapi_documentation_kwargs(),
)
app.include_router(router)
