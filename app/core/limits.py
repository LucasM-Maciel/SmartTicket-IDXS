"""HTTP/API bounds shared by Pydantic schemas and OpenAPI.

Training scripts read CSVs directly; they are not limited by these values
unless you add the same check there intentionally.
"""

from typing import Final

# Large enough for pasted emails / chat logs; small enough to reduce abuse
# and accidental memory pressure on a single request.
MAX_TICKET_TEXT_CHARS: Final[int] = 50_000
