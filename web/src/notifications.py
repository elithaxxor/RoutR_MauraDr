"""Mobile notification helpers."""
import logging
try:
    import requests
except ImportError:
    requests = None

logger = logging.getLogger(__name__)

PUSHBULLET_TOKEN = None


def send_pushbullet(title: str, body: str) -> bool:
    if not PUSHBULLET_TOKEN:
        logger.warning("Pushbullet token not configured")
        return False
    if not requests:
        logger.warning("requests module not available for Pushbullet notifications")
        return False
    try:
        resp = requests.post(
            'https://api.pushbullet.com/v2/pushes',
            json={'type': 'note', 'title': title, 'body': body},
            headers={'Access-Token': PUSHBULLET_TOKEN}
        )
        if resp.status_code == 200:
            logger.info("Notification sent")
            return True
        logger.error("Pushbullet error: %s", resp.text)
    except Exception as exc:
        logger.error("Failed to send notification: %s", exc)
    return False
