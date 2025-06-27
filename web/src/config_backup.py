import os
import subprocess
import logging
from typing import List
import difflib

logger = logging.getLogger(__name__)


def backup_config(ip: str, user: str, password: str, remote_path: str, dest_dir: str = "backups") -> str:
    """Backup the router configuration via SCP.

    Returns the path to the saved file on success or an empty string on failure.
    """
    os.makedirs(dest_dir, exist_ok=True)
    dest_file = os.path.join(dest_dir, f"{ip.replace('.', '_')}_config.backup")
    cmd = [
        "sshpass", "-p", password,
        "scp", "-o", "StrictHostKeyChecking=no",
        f"{user}@{ip}:{remote_path}", dest_file
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        logger.info("Backed up configuration from %s to %s", ip, dest_file)
        return dest_file
    except Exception as exc:
        logger.error("Failed to backup configuration: %s", exc)
        return ""


def verify_config(baseline_path: str, config_path: str) -> List[str]:
    """Compare a configuration file against a baseline.

    Returns a list of diff lines. An empty list means the files match.
    """
    if not os.path.exists(baseline_path):
        raise FileNotFoundError(f"Baseline {baseline_path} not found")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config {config_path} not found")

    with open(baseline_path, "r", encoding="utf-8") as f1, open(config_path, "r", encoding="utf-8") as f2:
        baseline_lines = f1.readlines()
        config_lines = f2.readlines()

    diff = list(difflib.unified_diff(baseline_lines, config_lines, fromfile="baseline", tofile="current", lineterm=""))
    return diff
