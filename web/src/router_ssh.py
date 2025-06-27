"""Attempt SSH login using default credentials."""
import subprocess
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

DEFAULT_CREDS: List[Tuple[str, str]] = [
    ("admin", "admin"),
    ("root", "root"),
    ("admin", "password"),
]


def attempt_default_credentials(ip: str, creds: List[Tuple[str, str]] = DEFAULT_CREDS) -> Tuple[str, str]:
    """Return the first successful credential pair or ("", "")."""
    for user, pwd in creds:
        cmd = [
            "sshpass", "-p", pwd,
            "ssh", "-o", "StrictHostKeyChecking=no",
            f"{user}@{ip}", "exit"
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5, check=True)
            logger.info("Successful SSH login on %s with %s/%s", ip, user, pwd)
            return user, pwd
        except subprocess.CalledProcessError:
            continue
        except Exception as exc:
            logger.debug("SSH attempt failed: %s", exc)
    return "", ""


def reboot_router(ip: str, user: str | None = None, password: str | None = None) -> bool:
    """Reboot the router via SSH.

    If ``user`` and ``password`` are not provided, ``attempt_default_credentials``
    will be used to discover working credentials.
    """
    if not user or not password:
        user, password = attempt_default_credentials(ip)
        if not user:
            logger.error("No valid SSH credentials found for %s", ip)
            return False
    cmd = [
        "sshpass",
        "-p",
        password,
        "ssh",
        "-o",
        "StrictHostKeyChecking=no",
        f"{user}@{ip}",
        "reboot",
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10, check=True)
        logger.info("Reboot command sent to %s", ip)
        return True
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Failed to reboot router %s: %s", ip, exc)
        return False
