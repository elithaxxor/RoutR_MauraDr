"""Import network inventory data to enrich scan results."""
import json
import logging
from typing import Dict, List

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
