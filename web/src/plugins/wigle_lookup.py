"""Plugin to query Wigle for wireless network details."""
from ..integrations.wigle import WigleClient

NAME = "WigleLookup"

client = WigleClient()

def register():
    return {"message": "Wigle plugin loaded", "credentials_set": bool(client.username and client.password)}
