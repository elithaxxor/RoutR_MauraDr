"""Firmware update check utilities."""
import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)
FIRMWARE_CACHE = Path(__file__).resolve().parent.parent / 'data' / 'firmware_cache.json'


def load_cache() -> dict:
    if FIRMWARE_CACHE.exists():
        with open(FIRMWARE_CACHE) as f:
            return json.load(f)
    return {}


def check_firmware_update(vendor: str, model: str, current_version: str) -> Optional[str]:
    """Return latest version if newer than current_version."""
    cache = load_cache()
    info = cache.get(vendor, {}).get(model)
    if not info:
        logger.warning("No firmware info for %s %s", vendor, model)
        return None
    latest = info.get('latest')
    if latest and latest != current_version:
        return latest
    return None
