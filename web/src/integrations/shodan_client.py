"""Simple Shodan API client used for importing scan results."""

import logging
from typing import List, Optional

try:
    import requests
except ImportError:
    requests = None

logger = logging.getLogger(__name__)
SHODAN_URL = "https://api.shodan.io"


def shodan_search(query: str, api_key: str) -> List[dict]:
    """Search Shodan with the provided query."""
    params = {"query": query, "key": api_key}
    try:
        resp = requests.get(f"{SHODAN_URL}/shodan/host/search", params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("matches", [])
    except Exception as exc:
        logger.error("Shodan search failed: %s", exc)
        return []


def shodan_host(ip: str, api_key: str) -> Optional[dict]:
    """Retrieve information for a specific host."""
    try:
        resp = requests.get(f"{SHODAN_URL}/shodan/host/{ip}", params={"key": api_key}, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        logger.error("Shodan host lookup failed: %s", exc)
        return None
