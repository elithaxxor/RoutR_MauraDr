import subprocess
import socket
import xml.etree.ElementTree as ET
from datetime import datetime
from .utils import validate_ip, validate_cidr
from .logging import setup_logger
from .config import config

logger = setup_logger(config['database'])

def discover_smb_hosts(network_cidr):
    """
    Discover SMB hosts in the given network CIDR using Nmap or manual socket checks.
    
    Args:
        network_cidr (str): Network range in CIDR notation (e.g., '192.168.1.0/24')
    
    Returns:
        list: List of IP addresses with SMB services
    """
    if not validate_cidr(network_cidr):
        logger.error(f"Invalid CIDR: {network_cidr}")
        return []

    logger.info(f"[*] Scanning network {network_cidr} for SMB hosts...")
    hosts = []
    try:
        nm_proc = subprocess.run(
            ["nmap", "-p", "445", "--open", "-n", "-T4", "-oG", "-", network_cidr],
            capture_output=True, text=True, check=True
        )
        for line in nm_proc.stdout.splitlines():
            if "/open/tcp//microsoft-ds" in line or "/open/tcp//netbios-ssn" in line:
                parts = line.split()
                if len(parts) > 1:
                    ip = parts[1]
                    hosts.append(ip)
    except subprocess.CalledProcessError as e:
        logger.warning(f"[!] Nmap scan failed: {e}. Falling back to manual scan.")
        base_net = network_cidr.rsplit('.', 1)[0] + '.'
        for i in range(1, 255):
            ip = base_net + str(i)
            for port in [139, 445]:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((ip, port))
                    sock.close()
                    if result == 0:
                        hosts.append(ip)
                        break
                except socket.error:
                    continue

    unique_hosts = sorted(set(hosts))
    for ip in unique_hosts:
        logger.info(f"Host {ip} has SMB service.")
    return unique_hosts

def run_nmap_scan(target, script_category=None, db_path="smb_enum.db", host_data=None):
    """
    Run an Nmap scan on the target and parse the results.
    
    Args:
        target (str): IP address to scan
        script_category (str, optional): Nmap script category to use
        db_path (str): Path to SQLite database
        host_data (dict, optional): Existing host data to update
    
    Returns:
        dict: Updated host data with scan results
    """
    if not validate_ip(target):
        logger.error(f"Invalid IP address: {target}")
        return host_data

    if host_data is None:
        host_data = {
            "vulnerabilities": [],
            "open_ports": [],
            "plaintext_creds": 0,
            "missing_patches": 0,
            "host": target
        }

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    xml_filename = f"nmap_results_{timestamp_str}_{target.replace('/', '_')}.xml"
    cmd = ["nmap", "-sV", "-p", "21,22,23,25,53,80,139,445,1433,3306,3389,5900,8080,8443", "-oX", xml_filename]

    if script_category:
        cmd += ["--script", script_category]
    cmd += [target]

    logger.info(f"[Nmap] Scanning {target} with script category: {script_category or 'None'}")
    try:
        subprocess.run(cmd, check=True)
        # Parse XML output
        tree = ET.parse(xml_filename)
        root = tree.getroot()
        for port in root.findall(".//port[@state='open']"):
            port_num = int(port.get('portid'))
            host_data["open_ports"].append(port_num)
            # Additional parsing for vulnerabilities could be added here
    except subprocess.CalledProcessError as e:
        logger.error(f"Nmap scan failed for {target}: {e}")
    except Exception as e:
        logger.error(f"Error parsing Nmap XML: {e}")

    return host_data
