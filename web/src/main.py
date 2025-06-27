from .config import config
from .logging import setup_logger
from .utils import (
    check_dependencies,
    validate_ip,
    validate_cidr,
    export_results,
    export_results_csv,
)
from .scanning import discover_smb_hosts, run_nmap_scan
from .enumeration import enumerate_lan_hosts
from .scoring import calculate_vulnerability_score, generate_remediation
from .plugin_loader import load_plugins
from .network_info import get_router_ip
from .config_backup import backup_config, verify_config
import os
import sys

logger = setup_logger(config['database'])

def display_help():
    """Display help information for the tool."""
    print("""
=== SMB-Scor3 Help ===
1) Discover and enumerate SMB hosts: Scan a network for SMB services and assess vulnerabilities.
3) Backup router configuration via SSH and SCP.
4) Verify configuration against a baseline file.
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

    # Load optional plugins using the plugin loader
    for plugin in load_plugins():
        try:
            plugin.register()
            logger.info(f"Loaded plugin: {plugin.name}")
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin.name}: {e}")

    while True:
        print("\n=== SMB-Scor3 MAIN MENU ===")
        print("1) Discover and enumerate SMB hosts")
        print("2) Help")
        print("3) Backup router configuration")
        print("4) Verify configuration against baseline")
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
                export_results(host_data, 'scan_results.json')
                export_results_csv(host_data, 'scan_results.csv')

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
        elif choice == '3':
            ip = input("Router IP [auto-detect]: ").strip() or get_router_ip()
            if not ip:
                print("Router IP not found.")
                continue
            user = input("SSH username [admin]: ").strip() or 'admin'
            password = input("SSH password: ").strip()
            remote = input("Remote config path [/etc/config.cfg]: ").strip() or '/etc/config.cfg'
            dest = input("Destination directory [backups]: ").strip() or 'backups'
            backup_config(ip, user, password, remote, dest)
        elif choice == '4':
            baseline = input("Baseline config file: ").strip()
            current = input("Config file to verify: ").strip()
            try:
                diff = verify_config(baseline, current)
                if not diff:
                    print("Configuration matches baseline.")
                else:
                    print('\n'.join(diff))
            except Exception as e:
                logger.error(f"Verification failed: {e}")
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
