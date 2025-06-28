import json
import logging
from pathlib import Path
from typing import Dict, Any, List

BASELINE_FILE = Path(__file__).resolve().parent.parent / "data" / "baseline.json"
logger = logging.getLogger(__name__)


def load_baseline() -> Dict[str, Any]:
    try:
        with open(BASELINE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        logger.debug("Failed to load baseline: %s", exc)
        return {}


def check_baseline(host_data: Dict[str, Dict[str, Any]], baseline: Dict[str, Any] | None = None) -> Dict[str, Dict[str, Any]]:
    baseline = baseline or load_baseline()
    closed_ports: List[int] = baseline.get("recommended_ports_closed", [])
    for host, info in host_data.items():
        risky = [p for p in closed_ports if p in info.get("open_ports", [])]
        if risky:
            info.setdefault("baseline_alerts", []).append(f"Open management ports: {risky}")
    return host_data
