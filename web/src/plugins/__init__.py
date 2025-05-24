"""Simple plugin system for RoutR_MauraDr.

Plugins can define a `register()` function which returns any commands or
handlers they want to expose. This allows extending the tool without
modifying the core code.
"""

import importlib
import pkgutil
import os
from typing import Dict, Any


def load_plugins(directory: str = os.path.join(os.path.dirname(__file__), '')) -> Dict[str, Any]:
    """Dynamically load all plugins in the given directory."""
    plugins: Dict[str, Any] = {}
    package = __package__
    for _, name, _ in pkgutil.iter_modules([directory]):
        module = importlib.import_module(f'{package}.{name}')
        if hasattr(module, 'register'):
            plugins[name] = module.register()
    return plugins
