from __future__ import annotations

"""Simple GPU monitoring utilities."""

import asyncio
import logging
import shutil
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


async def _run_cmd(cmd: List[str]) -> str:
    """Execute a command and capture stdout."""
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    out, _ = await proc.communicate()
    return out.decode()


async def query_nvidia_smi() -> Optional[List[Dict[str, Any]]]:
    """Return GPU stats using nvidia-smi if available."""
    if not shutil.which("nvidia-smi"):
        return None
    cmd = [
        "nvidia-smi",
        "--query-gpu=utilization.gpu,memory.used",
        "--format=csv,noheader,nounits",
    ]
    out = await _run_cmd(cmd)
    results = []
    for line in out.strip().splitlines():
        try:
            util, mem = [int(x) for x in line.split(',')]
            results.append({"util": util, "mem": mem})
        except Exception:  # pragma: no cover - defensive
            continue
    return results


async def query_rocm_smi() -> Optional[List[Dict[str, Any]]]:
    """Return GPU stats using rocm-smi if available."""
    if not shutil.which("rocm-smi"):
        return None
    out = await _run_cmd(["rocm-smi", "--showuse"],)
    results = []
    for line in out.strip().splitlines():
        if line.startswith("GPU") and "%" in line:
            parts = line.split()
            try:
                util = int(parts[2].rstrip('%'))
                mem = int(parts[5].rstrip('M'))
                results.append({"util": util, "mem": mem})
            except Exception:  # pragma: no cover - defensive
                continue
    return results


async def get_gpu_stats() -> List[Dict[str, Any]]:
    """Fetch GPU stats from available backend."""
    stats = await query_nvidia_smi()
    if stats is not None:
        return stats
    stats = await query_rocm_smi()
    return stats or []
