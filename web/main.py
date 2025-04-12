""" This module serves as the entry point, providing a menu-driven interface with enhanced usability. """

from .config import config
from .logging import setup_logger
from .utils import check_dependencies, validate_ip, validate_cidr
from .scanning import discover_smb_hosts, run_nmap_scan
from .enumeration import enumerate_lan_hosts
from .scoring import calculate_vulnerability_score, generate_remediation
import os
import sys

logger = setup_logger(config['database'])

def display_help():
    """Display help information for the tool."""
    print("""
=== SMB-Scor3 Help ===
1) Discover and enumerate SMB hosts: Scan a network for SMB services and assess vulnerabilities.
0) Exit: Quit the tool.

Tips:
- Enter a valid CIDR (e.g., '192.168.1.0/24') when prompted.
- Ensure required tools (nmap, crackmapexec, etc.) are installed.
""")

def main():
    """Main entry point for SMB-Scor3 Enhanced."""
    try:
        check_dependencies()
    except Exception as e:
        logger.error(f"Dependency check failed: {e}")
        sys.exit(1)

    while True:
        print("\n=== SMB-Scor3 MAIN MENU ===")
        print("1) Discover and enumerate SMB hosts")
        print("2) Help")
        print("0) Exit")
        choice = input("Select an option: ").strip()

        if choice == '0':
            logger.info("Exiting SMB-Scor3.")
            break
        elif choice == '2':
            display_help()
        elif choice == '1':
            network_cidr = input("Enter network CIDR (e.g., 192.168.1.0/24): ").strip()
            if not validate_cidr(network_cidr):
                logger.error("Invalid CIDR format. Example: 192.168.1.0/24")
                continue

            intensity = input("Enumeration intensity (low/medium/high, default=low): ").strip().lower() or "low"
            if intensity not in ["low", "medium", "high"]:
                logger.error("Invalid intensity. Using 'low'.")
                intensity = "low"

            try:
                # Discover SMB hosts
                hosts = discover_smb_hosts(network_cidr)
                if not hosts:
                    logger.warning("No SMB hosts found.")
                    continue

                # Enumerate hosts
                host_data = enumerate_lan_hosts(hosts, intensity)

                # Score and report
                for host, data in host_data.items():
                    score, category = calculate_vulnerability_score(data)
                    remediation = generate_remediation(data)
                    logger.info(f"{host}: Score={score}, Category={category}")
                    if remediation:
                        logger.info(f"Remediation for {host}:")
                        for step in remediation:
                            logger.info(f"  - {step}")

            except KeyboardInterrupt:
                logger.info("Operation cancelled by user.")
            except Exception as e:
                logger.error(f"An error occurred: {e}")
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
