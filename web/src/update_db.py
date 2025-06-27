"""Utility to update the local vulnerability database."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from urllib.request import urlopen

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CVE_DB = DATA_DIR / "cve_db.json"
DB_URL = "https://example.com/cve_db.json"

logger = logging.getLogger(__name__)


def update_database(url: str = DB_URL) -> bool:
    """Download the vulnerability database from ``url``."""
    try:
        with urlopen(url, timeout=10) as resp:
            data = json.load(resp)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(CVE_DB, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info("database updated from %s", url)
        return True
    except Exception as exc:  # pragma: no cover - network
        logger.error("db update failed: %s", exc)
        return False
