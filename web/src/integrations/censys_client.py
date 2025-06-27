import logging
from typing import Optional

try:
    import requests
except ImportError:
    requests = None

from ..config import config

CENSYS_BASE_URL = "https://search.censys.io/api"

logger = logging.getLogger(__name__)


class CensysClient:
    """Minimal Censys API client."""

    def __init__(self, api_id: Optional[str] = None, api_secret: Optional[str] = None) -> None:
        creds = config.get("censys", {})
        self.api_id = api_id or creds.get("id")
        self.api_secret = api_secret or creds.get("secret")
        if requests:
            self.session = requests.Session()
            if self.api_id and self.api_secret:
                self.session.auth = (self.api_id, self.api_secret)
            else:
                logger.warning("Censys credentials not configured")
        else:
            self.session = None
            logger.warning("requests module not available, CensysClient disabled")

    def _request(self, endpoint: str, **params):
        if not requests or not self.session:
            logger.warning("requests module not available for CensysClient requests")
            return None
        try:
            resp = self.session.get(f"{CENSYS_BASE_URL}{endpoint}", params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            logger.error("Censys request failed: %s", exc)
            return None

    def search_hosts(self, query: str):
        """Search hosts using the Censys search API."""
        return self._request("/v1/search/ipv4", q=query)

    def view_host(self, ip: str):
        """Retrieve details about a single host."""
        return self._request(f"/v1/view/ipv4/{ip}")
