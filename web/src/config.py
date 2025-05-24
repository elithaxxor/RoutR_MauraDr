import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'config.json')


def load_config():
    """Load configuration from config.json."""
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.json'))
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file {config_path} not found.")
    with open(config_path, 'r') as f:
        return json.load(f)


config = load_config()


def reload_config() -> None:
    """Reload configuration from disk."""
    global config
    config = load_config()
