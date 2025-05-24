import importlib
import pkgutil
from pathlib import Path

# Plugins live inside the web/src/plugins directory
PLUGIN_PATH = Path(__file__).resolve().parent / 'plugins'

class Plugin:
    """Simple plugin representation."""
    def __init__(self, module):
        self.module = module
        base = module.__name__.split('.')[-1]
        self.name = getattr(module, 'NAME', base)

    def register(self):
        return self.module.register() if hasattr(self.module, 'register') else None


def load_plugins():
    """Load all plugins in the plugins directory."""
    plugins = []
    if not PLUGIN_PATH.exists():
        return plugins
    for finder, name, ispkg in pkgutil.iter_modules([str(PLUGIN_PATH)]):
        module = importlib.import_module(f'web.src.plugins.{name}')
        plugins.append(Plugin(module))
    return plugins
