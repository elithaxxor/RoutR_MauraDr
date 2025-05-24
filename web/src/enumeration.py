from .utils import validate_ip
from .logging import setup_logger
from .config import config
from .scanning import run_nmap_scan
import subprocess

logger = setup_logger(config['database'])

def enumerate_lan_hosts(hosts, intensity="low"):
    """
    Enumerate SMB hosts with varying levels of intensity.
    
    Args:
        hosts (list): List of IP addresses to enumerate
        intensity (str): Enumeration intensity ('low', 'medium', 'high')
    
    Returns:
        dict: Host data with enumeration results
    """
    host_data = {}
    for ip in hosts:
        if not validate_ip(ip):
            logger.error(f"Invalid IP address: {ip}")
            continue
        host_data[ip] = {
            "vulnerabilities": [],
            "open_ports": [445],  # Assuming SMB is open
            "plaintext_creds": 0,
            "missing_patches": 0,
            "host": ip
        }
        
        try:
            # Base enumeration with crackmapexec
            cme = subprocess.run(
                ["crackmapexec", "smb", ip],
                capture_output=True, text=True, check=True
            )
            logger.info(f"[CME] {ip}: {cme.stdout}")
            if "SMBv1:True" in cme.stdout:
                host_data[ip]["vulnerabilities"].append("SMBv1 Enabled")

            if intensity == "medium":
                # Add enum4linux for more details
                e4l = subprocess.run(
                    ["enum4linux", ip],
                    capture_output=True, text=True, check=True
                )
                logger.info(f"[Enum4linux] {ip}: {e4l.stdout}")
                if "password without account" in e4l.stdout.lower():
                    host_data[ip]["plaintext_creds"] += 1

            elif intensity == "high":
                logger.info(f"[High Intensity] Running aggressive enumeration on {ip}")
                host_data[ip] = run_nmap_scan(ip, script_category="vuln", host_data=host_data[ip])

        except subprocess.CalledProcessError as e:
            logger.error(f"Enumeration failed for {ip}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during enumeration of {ip}: {e}")

    return host_data
