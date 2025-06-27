"""Import network inventory data to enrich scan results."""
import json
import logging
from typing import Dict, List, Tuple
from .scoring import calculate_vulnerability_score

logger = logging.getLogger(__name__)


def import_netbox(json_file: str) -> List[Dict[str, str]]:
    """Load device data exported from NetBox."""
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("devices", [])
    except Exception as exc:
        logger.error("Inventory import failed: %s", exc)
        return []


def enrich_results(results: Dict[str, Dict], inventory: List[Dict[str, str]]) -> Dict[str, Dict]:
    """Add inventory info to existing scan results."""
    inv_map = {d.get("ip"): d for d in inventory}
    for host, info in results.items():
        if host in inv_map:
            info.update({"device_name": inv_map[host].get("name")})
    return results


def prioritize_hosts(results: Dict[str, Dict]) -> List[Tuple[str, int]]:
    """Return hosts sorted by priority based on vulnerability score."""
    scored: List[Tuple[str, int]] = []
    for host, info in results.items():
        score, _ = calculate_vulnerability_score(info)
        priority = 100 - score
        scored.append((host, priority))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored
