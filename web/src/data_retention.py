"""Automatic pruning of old scan data."""
import logging
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


def prune_old_scans(results_dir: Path, days: int) -> int:
    """Delete scan files older than the given number of days."""
    cutoff = datetime.utcnow() - timedelta(days=days)
    removed = 0
    for path in results_dir.glob('*.json'):
        if datetime.utcfromtimestamp(path.stat().st_mtime) < cutoff:
            try:
                path.unlink()
                removed += 1
            except Exception:
                logger.warning("Failed to remove %s", path)
    return removed
