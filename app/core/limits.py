"""Shared bounds for ticket text length (API and offline training).

``MAX_TICKET_TEXT_CHARS`` is the single cap: ``POST /predict`` enforces it via
Pydantic; ``train_model`` drops CSV rows whose raw text exceeds it so training
and inference see the same upper bound.
"""

from typing import Final

# Large enough for pasted emails / chat logs; small enough to reduce abuse
# and accidental memory pressure on a single request.
MAX_TICKET_TEXT_CHARS: Final[int] = 50_000
