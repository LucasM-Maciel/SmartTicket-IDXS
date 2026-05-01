"""Send one test ticket to POST /predict (manual check that DB persistence works).

Set ``BASE_URL`` if not calling localhost (e.g. Railway). Requires the API process
to be running and, for a DB row, ``DATABASE_URL`` set where the server runs.

Usage::

    python scripts/post_test_ticket.py

    # Railway / staging
    set BASE_URL=https://your-service.up.railway.app
    python scripts/post_test_ticket.py
"""

from __future__ import annotations

import os
import sys
import uuid
from datetime import datetime, timezone

import httpx

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def main() -> int:
    marker = f"SMARTTICKET_DB_TEST_{uuid.uuid4().hex[:12]}"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    text = (
        f"[{marker}] Manual persistence check. "
        f"UTC={ts}. Customer reported slow Wi-Fi after a router firmware update."
    )
    url = f"{BASE_URL}/predict"
    try:
        response = httpx.post(url, json={"text": text}, timeout=60.0)
    except httpx.RequestError as e:
        print(f"Request failed: {e}", file=sys.stderr)
        print(f"Tried: POST {url}", file=sys.stderr)
        return 1

    print(f"POST {url} -> {response.status_code}")
    print(response.text)
    if response.is_success:
        print()
        print("Search in DB for this marker in text_raw (or copy the line above):")
        print(f"  {marker}")
    return 0 if response.is_success else 2


if __name__ == "__main__":
    raise SystemExit(main())
