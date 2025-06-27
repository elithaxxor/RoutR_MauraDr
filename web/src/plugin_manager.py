import json
from pathlib import Path
from typing import List, Tuple

from .plugin_marketplace import install_from_zip

PLUGIN_DIR = Path(__file__).resolve().parent / 'plugins'
ENABLED_FILE = PLUGIN_DIR / 'enabled.json'


def _load_enabled() -> List[str]:
    if ENABLED_FILE.exists():
        with open(ENABLED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def _save_enabled(enabled: List[str]) -> None:
    with open(ENABLED_FILE, 'w', encoding='utf-8') as f:
        json.dump(enabled, f, indent=2)


def list_plugins() -> List[Tuple[str, bool]]:
    """Return a list of (plugin_name, enabled) tuples."""
    enabled = set(_load_enabled())
    plugins = []
    for p in PLUGIN_DIR.glob('*.py'):
        if p.name == '__init__.py' or p.stem == 'enabled':
            continue
        plugins.append((p.stem, p.stem in enabled))
    return plugins


def enable_plugin(name: str) -> bool:
    enabled = set(_load_enabled())
    if name not in [p.stem for p in PLUGIN_DIR.glob('*.py')]:
        return False
    if name not in enabled:
        enabled.add(name)
        _save_enabled(sorted(enabled))
    return True


def disable_plugin(name: str) -> bool:
    enabled = set(_load_enabled())
    if name in enabled:
        enabled.remove(name)
        _save_enabled(sorted(enabled))
        return True
    return False


def install_plugin(url: str) -> bool:
    return install_from_zip(url)

