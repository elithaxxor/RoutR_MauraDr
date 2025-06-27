import json
from pathlib import Path
from typing import List, Dict

from .integrations.shodan_client import shodan_search, shodan_host
from .integrations.censys_client import CensysClient
from .integrations.wigle import WigleClient
from .utils import validate_ip

censys_client = CensysClient()
wigle_client = WigleClient()


def run_batch(file_path: str) -> List[Dict[str, object]]:
    """Perform batch lookups across Shodan, Censys and Wigle."""
    results = []
    lines = Path(file_path).read_text().splitlines()
    api_key = ''
    try:
        from .config import config
        api_key = config.get('shodan_api_key', '')
    except Exception:
        pass
    for line in lines:
        item = line.strip()
        if not item:
            continue
        entry = {'input': item}
        if validate_ip(item):
            entry['shodan'] = shodan_host(item, api_key) if api_key else None
            entry['censys'] = censys_client.view_host(item)
            entry['wigle'] = wigle_client.search_bssid(item)
        else:
            entry['shodan'] = shodan_search(item, api_key) if api_key else []
            entry['censys'] = censys_client.search_hosts(item)
            entry['wigle'] = wigle_client.search_ssid(item)
        results.append(entry)
    return results


def save_report(data: List[Dict[str, object]], output: str) -> str:
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return output
