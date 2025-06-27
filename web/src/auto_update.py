"""Check for updates to the companion app."""
import json
import logging
from urllib.request import urlopen

logger = logging.getLogger(__name__)

UPDATE_URL = "https://example.com/app/version.json"


def check_for_update(current_version: str) -> bool:
    """Return True if a newer version is available."""
    try:
        with urlopen(UPDATE_URL, timeout=5) as resp:
            data = json.load(resp)
    except Exception as exc:  # pragma: no cover - network
        logger.warning("Update check failed: %s", exc)
        return False
    latest = data.get("version")
    return latest is not None and latest != current_version
