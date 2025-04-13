#!/usr/bin/env python3
import os
import sys
import pwd
import grp
import subprocess
import logging
import shutil
from typing import List, Dict, TypedDict


# TODO: REFACTORING THE CODE SO IT'S MORE READABLE AND MAINTAINABLE
# TODO: ADD ERROR HANDLING AND LOGGING
# TODO: SILENTLY HANDLE ERRORS WHERE APPROPRIATE
# TODO: SILENT MODE OPTION


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HashData(TypedDict):
    LM: str
    NT: str


def get_smb_hashes() -> Dict[str, HashData]:
    """Retrieve SMB password hashes from the system."""
    try:
        # Check if running as root
        if os.geteuid() != 0:
            logger.error("Need root privileges to retrieve hashes")
            return {}

        hashes: Dict[str, HashData] = {}

        # Use pdbedit to get user list and hashes
        try:
            output = subprocess.check_output(
                ['pdbedit', '-L', '-w'],
                stderr=subprocess.PIPE
            ).decode()
            
            for line in output.splitlines():
                if ':' in line:
                    fields = line.split(':')
                    if len(fields) >= 4:
                        username = fields[0]
                        lm_hash = fields[2]
                        nt_hash = fields[3]
                        hashes[username] = {
                            'LM': lm_hash,
                            'NT': nt_hash
                        }
            logger.info(f"Successfully retrieved {len(hashes)} SMB hashes")
            return hashes
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to retrieve hashes using pdbedit: {e}")
            return {}

    except Exception as e:
        logger.error(f"Error retrieving SMB hashes: {e}")
        return {}


def check_root_privileges() -> bool:
    """Check if script is running with root privileges."""
    return os.geteuid() == 0


def install_samba() -> bool:
    """Install Samba and create backup of original configuration."""
    try:
        logger.info("Updating package lists...")
        subprocess.run(['apt-get', 'update'], check=True)
        
        logger.info("Installing Samba...")
        subprocess.run(['apt-get', 'install', '-y', 'samba'], check=True)
        
        # Backup original configuration
        shutil.copy('/etc/samba/smb.conf', '/etc/samba/smb.conf.bak')
        logger.info("Created backup of original Samba configuration")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install Samba: {e}")
        return False


def get_share_details() -> dict:
    """Get share configuration details from user input."""
    config = {}
    config['sharename'] = input("Enter name for the new share: ")
    config['sharepath'] = input("Enter full path to share directory: ")
    config['browseable'] = input(
        "Make share browseable? (yes/no) [no]: "
    ).lower() or 'no'
    config['writable'] = input(
        "Make share writable? (yes/no) [no]: "
    ).lower() or 'no'
    config['guestok'] = input(
        "Allow guest access? (yes/no) [no]: "
    ).lower() or 'no'
    return config


def setup_share_directory(path: str) -> bool:
    """Create and set up the share directory with proper permissions."""
    try:
        if not os.path.exists(path):
            create = input(
                "Path doesn't exist. Create it? (yes/no) [yes]: "
            ).lower() or 'yes'
            if create == 'yes':
                os.makedirs(path, exist_ok=True)
                logger.info(f"Created directory: {path}")
            else:
                logger.error("Aborting setup - directory not found")
                return False
        return True
    except Exception as e:
        logger.error(f"Failed to create directory: {e}")
        return False


def configure_samba_users() -> List[str]:
    """Configure Samba users and return list of configured usernames."""
    users = []
    while True:
        username = input(
            "Enter username for Samba access (leave empty to finish): "
        )
        if not username:
            break

        try:
            # Check if user exists
            subprocess.run(['id', username], check=True)
        except subprocess.CalledProcessError:
            create_user = input(
                "User doesn't exist. Create new system user? (yes/no) [no]: "
            ).lower() or 'no'
            if create_user == 'yes':
                try:
                    subprocess.run(
                        ['useradd', '-m', '-s', '/usr/sbin/nologin', username],
                        check=True
                    )
                    subprocess.run(['passwd', '-l', username], check=True)
                except subprocess.CalledProcessError as e:
                    logger.error(f"Failed to create system user: {e}")
                    continue

        try:
            # Add to Samba
            subprocess.run(['smbpasswd', '-L', '-a', username], check=True)
            subprocess.run(['smbpasswd', '-L', '-e', username], check=True)
            users.append(username)
            logger.info(f"Successfully added Samba user: {username}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to configure Samba user: {e}")

    return users


def create_samba_config(config: dict, users: List[str]) -> bool:
    """Create Samba configuration file with secure settings."""
    try:
        with open('/etc/samba/smb.conf', 'w') as f:
            f.write("""[global]
   workgroup = WORKGROUP
   server role = standalone server
   security = user
   map to guest = bad user
   smb encrypt = required
   min protocol = SMB2_02
   unix password sync = yes
   log file = /var/log/samba/log.%m
   max log size = 1000
   logging = file
   panic action = /usr/share/samba/panic-action %d
   server multi channel support = yes

""")

            # Write share configuration
            f.write(f"""[{config['sharename']}]
   path = {config['sharepath']}
   browseable = {config['browseable']}
   writable = {config['writable']}
   guest ok = {config['guestok']}
""")

            # Add user restrictions if needed
            if config['guestok'] == 'no' and users:
                f.write(f"   valid users = {' '.join(users)}\n")

        logger.info("Created Samba configuration file")
        return True
    except Exception as e:
        logger.error(f"Failed to create Samba configuration: {e}")
        return False


def set_permissions(config: dict, users: List[str]) -> None:
    """Set appropriate permissions on share directory."""
    try:
        if config['guestok'] == 'no' and users:
            os.chown(
                config['sharepath'],
                pwd.getpwnam(users[0]).pw_uid,
                grp.getgrnam(users[0]).gr_gid
            )
            # SGID to maintain group ownership
            os.chmod(config['sharepath'], 0o2770)
        else:
            os.chmod(config['sharepath'], 0o2777)
            logger.warning("Share is world-writable!")
    except Exception as e:
        logger.error(f"Failed to set permissions: {e}")


def ensure_persistence() -> bool:
    """Ensure Samba service persistence through systemd."""
    try:
        subprocess.run(['systemctl', 'enable', 'smbd'], check=True)
        subprocess.run(['systemctl', 'restart', 'smbd'], check=True)
        logger.info("Enabled and started Samba service")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to configure service persistence: {e}")
        return False


def verify_configuration() -> bool:
    """Verify Samba configuration."""
    try:
        subprocess.run(['testparm', '-s'], check=True)
        logger.info("Samba configuration verified successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Configuration verification failed: {e}")
        return False


def display_share_info(share_name: str) -> None:
    """Display share access information."""
    try:
        host_ip = subprocess.check_output(
            ['hostname', '-I']
        ).decode().split()[0]
        hostname = subprocess.check_output(['hostname']).decode().strip()
        hostname = hostname.split('.')[0]
        print("\nSamba setup complete!")
        print("Share accessible at:")
        print(f"  Host: {host_ip}")
        print(f"  Share: \\\\{hostname}\\{share_name}")
    except Exception as e:
        logger.error(f"Failed to display share information: {e}")


def main() -> None:
    """Main function to orchestrate Samba setup."""
    print("[+] Welcome to the Samba setup script!")
    
    if not check_root_privileges():
        logger.error("Please run this script as root")
        sys.exit(1)

    if not install_samba():
        print("[-] Failed to install Samba. Exiting.")
        sys.exit(1)

    config = get_share_details()
    
    if not setup_share_directory(config['sharepath']):
        sys.exit(1)

    users = configure_samba_users()
    
    if not create_samba_config(config, users):
        sys.exit(1)
        
    set_permissions(config, users)
    
    if not ensure_persistence():
        sys.exit(1)
        
    if not verify_configuration():
        sys.exit(1)
        
    display_share_info(config['sharename'])

    # Retrieve and display SMB hashes
    print("\n[+] Retrieving SMB password hashes...")
    hashes = get_smb_hashes()
    if hashes:
        print("\nSMB Password Hashes:")
        for username, hash_data in hashes.items():
            print(f"User: {username}")
            print(f"LM Hash: {hash_data['LM']}")
            print(f"NT Hash: {hash_data['NT']}")
            print("-" * 50)
    else:
        print("[-] No SMB hashes retrieved")


if __name__ == "__main__":
    main()
