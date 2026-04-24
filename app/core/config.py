"""ML artifact paths, dataset path, and CSV column names (training / inference).

HTTP request bounds (e.g. max `text` length) live in ``app.core.limits``.

Optional overrides (paths as strings, absolute or relative to process CWD):

- ``SMARTTICKET_MODEL_PATH``
- ``SMARTTICKET_VECTORIZER_PATH``
- ``SMARTTICKET_DATASET_PATH``
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
