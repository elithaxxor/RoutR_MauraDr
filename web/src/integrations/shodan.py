import logging
from typing import Optional
try:
    import requests
except ImportError:
    requests = None
from ..config import config

SHODAN_BASE_URL = "https://api.shodan.io"

logger = logging.getLogger(__name__)

class ShodanClient:
    """Simple wrapper around the Shodan API."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or config.get("shodan_api_key")
        if requests:
            self.session = requests.Session()
        else:
            self.session = None
            logger.warning("requests module not available, ShodanClient disabled")

    def _request(self, endpoint: str, **params):
        if not self.api_key:
            logger.warning("Shodan API key not configured")
            return None
        params["key"] = self.api_key
        if not requests or not self.session:
            logger.warning("requests module not available for ShodanClient requests")
            return None
        try:
            resp = self.session.get(f"{SHODAN_BASE_URL}{endpoint}", params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            logger.error("Shodan request failed: %s", exc)
            return None

    def search(self, query: str):
        """Search Shodan with the given query."""
        return self._request("/shodan/host/search", query=query)

    def host(self, ip: str):
        """Retrieve information about a single host."""
        return self._request(f"/shodan/host/{ip}")
