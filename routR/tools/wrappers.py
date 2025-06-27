"""Wrappers for external CLI tools used by RoutR_MauraDr."""

from __future__ import annotations

import asyncio
import logging
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def _which(cmd: str) -> Optional[str]:
    """Return full path of command if available."""
    return shutil.which(cmd)


def is_available(cmd: str) -> bool:
    """Check if a CLI tool is present on the system."""
    return _which(cmd) is not None


async def _run_tool(cmd: List[str]) -> Dict[str, Any]:
    """Execute an external command asynchronously and capture output."""
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        return {
            "cmd": cmd,
            "returncode": proc.returncode,
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
        }
    except FileNotFoundError:
        return {"error": f"{cmd[0]} not found"}
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("failed running %s: %s", cmd, exc)
        return {"error": str(exc)}


async def run_masscan(target: str, ports: str = "1-1024") -> Dict[str, Any]:
    if not is_available("masscan"):
        return {"error": "masscan missing"}
    return await _run_tool(
        ["masscan", target, "-p", ports, "--rate", "1000", "-oJ", "-"]
    )


async def run_arp_scan(interface: str = "eth0") -> Dict[str, Any]:
    if not is_available("arp-scan"):
        return {"error": "arp-scan missing"}
    return await _run_tool(["arp-scan", "--localnet", "-I", interface])


async def run_hydra(
    target: str, service: str, userlist: str, passlist: str
) -> Dict[str, Any]:
    if not is_available("hydra"):
        return {"error": "hydra missing"}
    return await _run_tool(["hydra", "-L", userlist, "-P", passlist, target, service])


async def run_gvm_cli(script: str) -> Dict[str, Any]:
    if not is_available("gvm-cli"):
        return {"error": "gvm-cli missing"}
    return await _run_tool(["gvm-cli", "ssh", "--", script])


async def run_miniupnpc() -> Dict[str, Any]:
    cmd = _which("upnpc") or _which("miniupnpc")
    if not cmd:
        return {"error": "miniupnpc missing"}
    return await _run_tool([cmd, "-l"])


async def run_nikto(target: str) -> Dict[str, Any]:
    if not is_available("nikto"):
        return {"error": "nikto missing"}
    return await _run_tool(["nikto", "-h", target, "-o", "-", "-Format", "json"])


async def run_sqlmap(url: str) -> Dict[str, Any]:
    if not is_available("sqlmap"):
        return {"error": "sqlmap missing"}
    return await _run_tool(
        ["sqlmap", "-u", url, "--batch", "--output-dir", str(Path(".").resolve())]
    )


async def run_pgrok(port: int) -> Dict[str, Any]:
    if not is_available("pgrok"):
        return {"error": "pgrok missing"}
    return await _run_tool(["pgrok", "http", str(port)])
