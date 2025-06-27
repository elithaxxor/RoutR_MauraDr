import importlib
import pkgutil
import json
from pathlib import Path

# Plugins live inside the web/src/plugins directory
PLUGIN_PATH = Path(__file__).resolve().parent / 'plugins'
ENABLED_FILE = PLUGIN_PATH / 'enabled.json'

class Plugin:
    """Simple plugin representation."""
    def __init__(self, module):
        self.module = module
        base = module.__name__.split('.')[-1]
        self.name = getattr(module, 'NAME', base)

    def register(self):
        return self.module.register() if hasattr(self.module, 'register') else None


def _enabled_names():
    if ENABLED_FILE.exists():
        try:
            with open(ENABLED_FILE, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()


def load_plugins():
    """Load all plugins in the plugins directory."""
    plugins = []
    if not PLUGIN_PATH.exists():
        return plugins
    enabled = _enabled_names()
    for _, name, _ in pkgutil.iter_modules([str(PLUGIN_PATH)]):
        if name == 'enabled':
            continue
        if enabled and name not in enabled:
            continue
        module = importlib.import_module(f'web.src.plugins.{name}')
        plugins.append(Plugin(module))
    return plugins
