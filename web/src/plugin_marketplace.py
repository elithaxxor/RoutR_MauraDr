"""Helpers for downloading and installing community plugins."""
import logging
import zipfile
from urllib.request import urlopen
from io import BytesIO
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parent / 'plugins'
logger = logging.getLogger(__name__)


def install_from_zip(url: str) -> bool:
    """Download a zipped plugin from a URL and extract it."""
    try:
        with urlopen(url) as resp:
            data = resp.read()
        with zipfile.ZipFile(BytesIO(data)) as zf:
            zf.extractall(PLUGIN_DIR)
        logger.info("Plugin installed from %s", url)
        return True
    except Exception as exc:
        logger.error("Failed to install plugin: %s", exc)
        return False


def list_installed() -> list:
    return [p.stem for p in PLUGIN_DIR.glob('*.py') if p.name != '__init__.py']

