"""Correlate local scan results with Shodan and Censys data."""
import logging
from typing import Dict

from .integrations.shodan import ShodanClient
from .integrations.censys_client import CensysClient

logger = logging.getLogger(__name__)


def correlate_hosts(results: Dict[str, Dict]) -> Dict[str, Dict]:
    """Fetch external data and compare with local results."""
    shodan = ShodanClient()
    censys = CensysClient()
    for ip, info in results.items():
        discrepancies = []

        shodan_data = shodan.host(ip) if shodan else None
        if shodan_data:
            open_ports = [d.get("port") for d in shodan_data.get("data", [])]
            info["shodan_ports"] = open_ports
            for port in open_ports:
                if port not in info.get("open_ports", []):
                    discrepancies.append(f"Shodan:{port}")

        censys_data = censys.view_host(ip)
        if censys_data:
            c_ports = [svc.get("port") for svc in censys_data.get("services", [])]
            info["censys_ports"] = c_ports
            for port in c_ports:
                if port not in info.get("open_ports", []):
                    discrepancies.append(f"Censys:{port}")

        if discrepancies:
            info["external_discrepancies"] = discrepancies
    return results
