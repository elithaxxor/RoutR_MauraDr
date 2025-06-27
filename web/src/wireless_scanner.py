"""Simple 802.11 wireless scanner wrappers."""
import subprocess
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def scan_networks(interface: str = "wlan0") -> List[Dict[str, str]]:
    """Return a list of detected Wi-Fi networks using iwlist."""
    try:
        output = subprocess.check_output(["iwlist", interface, "scanning"], text=True)
    except Exception as exc:
        logger.error("Wi-Fi scan failed: %s", exc)
        return []

    networks = []
    essid = None
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("Cell"):
            essid = None
        if "ESSID:" in line:
            essid = line.split(":", 1)[1].strip().strip('"')
        if "Encryption key:" in line and essid:
            enc = line.split(":", 1)[1].strip()
            networks.append({"ssid": essid, "encryption": enc})
    return networks


def capture_handshake(interface: str, bssid: str, output_prefix: str = "capture") -> bool:
    """Run airodump-ng to capture a WPA handshake."""
    try:
        subprocess.Popen([
            "airodump-ng",
            "--bssid",
            bssid,
            "-w",
            output_prefix,
            interface,
        ])
        logger.info("Started handshake capture on %s", bssid)
        return True
    except Exception as exc:
        logger.error("Failed to capture handshake: %s", exc)
        return False
