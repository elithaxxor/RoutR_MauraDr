"""IPv6 network discovery utilities."""
import subprocess
import logging
from typing import List

logger = logging.getLogger(__name__)


def discover_ipv6_hosts(cidr: str) -> List[str]:
    """Discover IPv6 hosts using nmap."""
    try:
        result = subprocess.check_output([
            'nmap', '-6', '-sn', cidr, '-oG', '-'
        ], text=True)
    except Exception as exc:
        logger.error("IPv6 discovery failed: %s", exc)
        return []
    hosts = []
    for line in result.splitlines():
        if line.startswith('Host:') and 'Status: Up' in line:
            parts = line.split()
            if len(parts) >= 2:
                hosts.append(parts[1])
    return hosts

