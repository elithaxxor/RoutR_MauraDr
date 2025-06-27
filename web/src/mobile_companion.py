"""Utilities for sending scan summaries to mobile devices."""
import logging
from .notifications import send_pushbullet

logger = logging.getLogger(__name__)


def send_summary(title: str, summary: str) -> bool:
    """Send a brief summary using the configured notification channel."""
    logger.info("Sending mobile summary: %s", title)
    return send_pushbullet(title, summary)

