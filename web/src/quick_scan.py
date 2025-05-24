"""Quick port scanning helpers."""
import subprocess
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def quick_scan(target: str, out_prefix: str = "quick_scan") -> Path:
    """Run a SYN scan on top 10 ports with OS detection."""
    txt = Path(f"{out_prefix}.txt")
    js = Path(f"{out_prefix}.json")
    cmd = [
        "nmap", "-sS", "-n", "--top-ports", "10", "-O", target
    ]
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode()
        txt.write_text(result)
        open_ports = []
        for line in result.splitlines():
            if "/tcp" in line and "open" in line:
                port = line.split("/tcp")[0].strip()
                if port.isdigit():
                    open_ports.append(int(port))
        json.dump({"target": target, "open_ports": open_ports}, js.open("w"))
        return js
    except Exception as exc:
        logger.error("Quick scan failed: %s", exc)
        return js
