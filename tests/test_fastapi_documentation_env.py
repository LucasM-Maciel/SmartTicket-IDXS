"""Env-driven FastAPI documentation toggle (``SMARTTICKET_DISABLE_OPENAPI``)."""

from __future__ import annotations

import pytest

from app.core.config import fastapi_documentation_kwargs


@pytest.mark.parametrize(
    "value",
    ["1", "true", "yes", "TRUE", " True "],
)
def test_fastapi_documentation_disabled_when_truthy(
    monkeypatch: pytest.MonkeyPatch, value: str
) -> None:
    monkeypatch.setenv("SMARTTICKET_DISABLE_OPENAPI", value)
    assert fastapi_documentation_kwargs() == {
        "docs_url": None,
        "redoc_url": None,
        "openapi_url": None,
    }


def test_fastapi_documentation_enabled_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("SMARTTICKET_DISABLE_OPENAPI", raising=False)
    assert fastapi_documentation_kwargs() == {}


def test_fastapi_documentation_enabled_for_unknown_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SMARTTICKET_DISABLE_OPENAPI", "0")
    assert fastapi_documentation_kwargs() == {}
