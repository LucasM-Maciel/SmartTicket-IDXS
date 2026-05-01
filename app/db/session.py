"""Database engine and session factory.

``DATABASE_URL`` is read from the environment (typically via ``.env`` loaded in
``app.main``). If unset, ``get_engine()`` returns ``None``, ``get_db`` yields
``None``, and ``POST /predict`` responds with 503 (persistence required). Tests
override ``get_db`` or unset ``DATABASE_URL`` and inject a fake session.
"""

from __future__ import annotations

import os
from collections.abc import Generator
from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine

_engine: Engine | None = None
_no_url_after_check = False
SessionLocal: sessionmaker[Session] | None = None


def reset_db_engine_state() -> None:
    """Dispose engine and clear cached factory (for tests / config changes)."""
    global _engine, _no_url_after_check, SessionLocal
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _no_url_after_check = False
    SessionLocal = None


def get_engine() -> Engine | None:
    global _engine, _no_url_after_check, SessionLocal
    if _engine is not None:
        return _engine
    if _no_url_after_check:
        return None
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        _no_url_after_check = True
        return None
    eng = create_engine(url, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=eng)
    _engine = eng
    return eng


def get_db() -> Generator[Session | None, None, None]:
    get_engine()
    if SessionLocal is None:
        yield None
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
