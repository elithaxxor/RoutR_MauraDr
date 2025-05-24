"""Helpers for starting netcat and ngrok."""
import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def start_netcat_listener(port: int = 6666) -> Optional[subprocess.Popen]:
    try:
        proc = subprocess.Popen([
            "nc", "-lvp", str(port)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("Netcat listening on %d", port)
        return proc
    except Exception as exc:
        logger.error("Failed to start netcat: %s", exc)
        return None


def start_ngrok_tcp(port: int = 6667) -> Optional[subprocess.Popen]:
    try:
        proc = subprocess.Popen([
            "ngrok", "tcp", str(port), "--log=stdout"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("ngrok tcp tunnel on %d", port)
        return proc
    except Exception as exc:
        logger.error("Failed to start ngrok tcp: %s", exc)
        return None


def start_ngrok_http(port: int = 80) -> Optional[subprocess.Popen]:
    try:
        proc = subprocess.Popen([
            "ngrok", "http", str(port), "--log=stdout"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("ngrok http tunnel on %d", port)
        return proc
    except Exception as exc:
        logger.error("Failed to start ngrok http: %s", exc)
        return None
