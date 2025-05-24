import base64
import logging
from typing import Optional
import requests
from ..config import config

WIGLE_BASE_URL = "https://api.wigle.net/api/v2"

logger = logging.getLogger(__name__)

class WigleClient:
    """Client for interacting with the Wigle API."""

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None) -> None:
        creds = config.get("wigle", {})
        self.username = username or creds.get("username")
        self.password = password or creds.get("password")
        self.session = requests.Session()
        if self.username and self.password:
            token = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
            self.session.headers.update({"Authorization": f"Basic {token}"})
        else:
            logger.warning("Wigle credentials not configured")

    def _request(self, endpoint: str, **params):
        try:
            resp = self.session.get(f"{WIGLE_BASE_URL}{endpoint}", params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            logger.error("Wigle request failed: %s", exc)
            return None

    def search_ssid(self, ssid: str):
        """Search for networks matching a specific SSID."""
        return self._request("/network/search", ssid=ssid)

    def search_bssid(self, bssid: str):
        """Search for a network by BSSID/MAC address."""
        return self._request("/network/search", netid=bssid)
