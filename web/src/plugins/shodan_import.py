"""Plugin to import results from Shodan."""
from ..integrations.shodan import ShodanClient

NAME = "ShodanImport"

client = ShodanClient()

def register():
    return {"message": "Shodan plugin loaded", "api_key_set": bool(client.api_key)}
  """Plugin to import scan results from Shodan."""

from ..integrations import shodan_client
from ..config import config

NAME = "ShodanImport"


def register():
    api_key = config.get("shodan_api_key")
    if not api_key:
        return {"error": "Shodan API key not configured"}
    query = config.get("default_shodan_query", "net:192.168.1.0/24")
    results = shodan_client.shodan_search(query, api_key)
    return {"count": len(results), "sample": results[:5]}
