"""Network information gathering utilities for RoutR_MauraDr."""
import logging
import subprocess
import re
import requests

logger = logging.getLogger(__name__)


def _run_cmd(cmd: str) -> str:
    """Helper to run a shell command and return output."""
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
        return out.decode().strip()
    except Exception as exc:
        logger.debug("Command failed %s: %s", cmd, exc)
        return ""


def get_local_ip() -> str:
    """Return the first non-loopback IP address."""
    return _run_cmd("ip route get 1.1.1.1 | awk '{print $7; exit}'")


def get_router_ip() -> str:
    """Return the default gateway IP."""
    return _run_cmd("ip route | awk '/default/ {print $3; exit}'")


def get_wan_ip() -> str:
    """Return the external IP using ipify."""
    try:
        resp = requests.get("https://api64.ipify.org", timeout=5)
        return resp.text.strip()
    except Exception as exc:
        logger.warning("Failed to fetch WAN IP: %s", exc)
        return ""


def get_dns_servers() -> list:
    """Return list of DNS servers from /etc/resolv.conf."""
    data = _run_cmd("awk '/^nameserver/ {print $2}' /etc/resolv.conf")
    return [s for s in data.splitlines() if s]


def get_subnet_mask() -> str:
    out = _run_cmd("ifconfig 2>/dev/null | grep -w 'netmask' | head -n 1")
    m = re.search(r'netmask (\S+)', out)
    return m.group(1) if m else ""


def get_router_mac() -> str:
    router_ip = get_router_ip()
    if not router_ip:
        return ""
    out = _run_cmd(f"arp -n {router_ip}")
    m = re.search(r'(..:..:..:..:..:..)', out)
    return m.group(1) if m else ""


def arp_table() -> list:
    """Return list of dicts with ip, mac, and hostname from arp table."""
    out = _run_cmd("arp -a")
    entries = []
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 4:
            ip = parts[1].strip('()')
            mac = parts[3]
            host = parts[0]
            entries.append({'ip': ip, 'mac': mac, 'hostname': host})
    return entries


def get_router_dns_table() -> list:
    """Attempt to gather local DNS entries via SNMP/UPnP/brute force."""
    router = get_router_ip()
    if not router:
        return []
    results = []
    snmp = _run_cmd(f"snmpwalk -v2c -c public {router} 2>/dev/null | grep -i dns")
    for line in snmp.splitlines():
        m = re.search(r'((?:\d+\.){3}\d+).*?(\w[^ ]+)', line)
        if m:
            results.append({'ip': m.group(1), 'hostname': m.group(2)})
    upnp = _run_cmd("upnpc -l 2>/dev/null")
    for line in upnp.splitlines():
        m = re.search(r'((?:\d+\.){3}\d+).*?(\w[^ ]+)', line)
        if m:
            results.append({'ip': m.group(1), 'hostname': m.group(2)})
    # simple brute force - look up same subnet
    subnet = '.'.join(router.split('.')[:3])
    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        host = _run_cmd(f"nslookup {ip} {router} 2>/dev/null | awk '/name =/ {{print $4}}' | sed 's/.$//'")
        if host:
            results.append({'ip': ip, 'hostname': host})
    # deduplicate
    dedup = {(r['ip'], r['hostname']): r for r in results}
    return list(dedup.values())


def get_router_make_model() -> str:
    router = get_router_ip()
    if not router:
        return ""
    try:
        resp = requests.get(f"http://{router}", timeout=3)
        text = resp.text.lower()
        keywords = ["netgear", "tp-link", "asus", "linksys", "d-link", "cisco", "arris", "motorola", "ubiquiti", "mikrotik"]
        for kw in keywords:
            if kw in text:
                return kw.capitalize()
    except Exception as exc:
        logger.debug("Router make/model fetch failed: %s", exc)
    return ""


def get_router_firmware() -> str:
    router = get_router_ip()
    if not router:
        return ""
    out = _run_cmd(f"snmpwalk -v2c -c public {router} 1.3.6.1.2.1.1.1.0")
    m = re.search(r'\s([\w\-.]+)$', out)
    if m:
        return m.group(1)
    try:
        resp = requests.get(f"http://{router}", timeout=3)
        m = re.search(r'Firmware Version[: ]*([0-9A-Za-z.\-]+)', resp.text)
        if m:
            return m.group(1)
    except Exception:
        pass
    upnp = _run_cmd("upnpc -l 2>/dev/null | grep -i firmware")
    m = re.search(r'Firmware[\w ]*:\s*([0-9A-Za-z.\-]+)', upnp)
    return m.group(1) if m else ""


from pathlib import Path
import json

CVE_DB = Path(__file__).resolve().parent.parent / 'data' / 'cve_db.json'


def lookup_firmware_cve(vendor: str, version: str) -> list:
    """Return CVE list for the given vendor and firmware version."""
    if not CVE_DB.exists():
        return []
    with open(CVE_DB, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get(vendor, {}).get(version, [])

