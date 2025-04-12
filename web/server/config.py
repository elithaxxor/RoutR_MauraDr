import json
import os

CONFIG_FILE = 'config.json'

def load_config():
    """Load configuration from config.json."""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Configuration file {CONFIG_FILE} not found.")
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

config = load_config()
