"""Plugin to import results from Shodan."""
from ..integrations.shodan import ShodanClient

NAME = "ShodanImport"

client = ShodanClient()

def register():
    return {"message": "Shodan plugin loaded", "api_key_set": bool(client.api_key)}
