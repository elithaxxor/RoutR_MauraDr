import subprocess
import json
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def list_outdated() -> List[Dict[str, str]]:
    """Return a list of outdated Python packages using pip."""
    try:
        result = subprocess.check_output([
            "pip",
            "list",
            "--outdated",
            "--format",
            "json",
        ], text=True)
        return json.loads(result)
    except Exception as exc:
        logger.error("Failed to list outdated packages: %s", exc)
        return []


def update_packages(packages: List[str]) -> bool:
    """Attempt to update the given packages."""
    if not packages:
        return False
    try:
        subprocess.check_call(["pip", "install", "--upgrade", *packages])
        logger.info("Updated packages: %s", ", ".join(packages))
        return True
    except Exception as exc:
        logger.error("Package update failed: %s", exc)
        return False
