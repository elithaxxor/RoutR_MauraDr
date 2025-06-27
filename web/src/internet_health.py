from __future__ import annotations

"""Simple internet connectivity monitor with auto-reboot."""

import subprocess
import time
import logging
from typing import Optional

from .notifications import send_pushbullet
from .network_info import get_router_ip
from .router_ssh import reboot_router

logger = logging.getLogger(__name__)


def check_connectivity(host: str = "8.8.8.8") -> bool:
    """Return True if the host is reachable via ping."""
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Connectivity check failed: %s", exc)
        return False


def monitor(
    router_ip: Optional[str] = None,
    interval: int = 60,
    threshold: int = 3,
    iterations: Optional[int] = None,
) -> None:
    """Monitor connectivity and reboot router on repeated failure."""
    router_ip = router_ip or get_router_ip()
    fails = 0
    count = 0
    while iterations is None or count < iterations:
        if check_connectivity():
            fails = 0
        else:
            fails += 1
            logger.warning("Connectivity check failed (%s/%s)", fails, threshold)
            if fails >= threshold:
                if router_ip:
                    reboot_router(router_ip)
                send_pushbullet(
                    "RoutR: Connectivity Issue",
                    "Internet unreachable, reboot triggered",
                )
                fails = 0
        count += 1
        time.sleep(interval)
