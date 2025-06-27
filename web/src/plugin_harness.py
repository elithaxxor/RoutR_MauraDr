"""Simple testing harness for RoutR plugins."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Dict, Iterable


def validate_plugin(path: Path) -> bool:
    """Load a plugin file and run its ``register`` method."""
    spec = importlib.util.spec_from_file_location("plugin", path)
    if not spec or not spec.loader:
        return False
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        return False
    if not hasattr(module, "register"):
        return False
    try:
        result = module.register()
        return isinstance(result, dict)
    except Exception:
        return False


def run_tests(paths: Iterable[Path]) -> Dict[str, bool]:
    """Validate all plugin paths and return a mapping of path to result."""
    return {str(p): validate_plugin(p) for p in paths}
