"""ML artifact paths, dataset path, CSV column names, and small env toggles.

HTTP request bounds (e.g. max `text` length) live in ``app.core.limits``.

Optional path overrides (strings, absolute or relative to process CWD):

- ``SMARTTICKET_MODEL_PATH``
- ``SMARTTICKET_VECTORIZER_PATH``
- ``SMARTTICKET_DATASET_PATH``

Optional app assembly:

- ``SMARTTICKET_DISABLE_OPENAPI`` — hide ``/docs``, ``/redoc``, OpenAPI JSON (see ``fastapi_documentation_kwargs``).
"""

import os
from pathlib import Path
from typing import Final

_REPO_ROOT: Final[Path] = Path(__file__).resolve().parent.parent.parent


def _path_from_env(key: str, default: Path) -> Path:
    raw = os.environ.get(key)
    return Path(raw).expanduser() if raw else default


MODEL_PATH: Final[Path] = _path_from_env(
    "SMARTTICKET_MODEL_PATH",
    _REPO_ROOT / "artifacts" / "model.pkl",
)
VECTORIZER_PATH: Final[Path] = _path_from_env(
    "SMARTTICKET_VECTORIZER_PATH",
    _REPO_ROOT / "artifacts" / "vectorizer.pkl",
)
DATASET_PATH: Final[Path] = _path_from_env(
    "SMARTTICKET_DATASET_PATH",
    _REPO_ROOT / "app" / "data" / "raw" / "customer_support_tickets.csv",
)

TEXT_COLUMN: Final[str] = "Ticket Description"
LABEL_COLUMN: Final[str] = "Ticket Type"


def fastapi_documentation_kwargs() -> dict[str, str | None]:
    """Kwargs for ``FastAPI(...)`` to drop public schema UIs when env asks for it.

    Truthy ``SMARTTICKET_DISABLE_OPENAPI``: ``1``, ``true``, ``yes`` (case-insensitive).
    Default: empty dict — docs stay enabled for local development.
    """
    v = (os.environ.get("SMARTTICKET_DISABLE_OPENAPI") or "").strip().lower()
    if v in ("1", "true", "yes"):
        return {"docs_url": None, "redoc_url": None, "openapi_url": None}
    return {}
