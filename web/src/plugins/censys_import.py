"""Plugin to import scan results from Censys."""
from ..integrations.censys_client import CensysClient
from ..config import config

NAME = "CensysImport"

client = CensysClient()

def register():
    query = config.get("default_censys_query", "services.service_name:HTTP")
    results = client.search_hosts(query)
    count = len(results.get('results', [])) if isinstance(results, dict) else 0
    return {"count": count, "sample": results.get('results', [])[:5] if isinstance(results, dict) else []}
