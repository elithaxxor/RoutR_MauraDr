import subprocess
import shutil
import ipaddress
import re
import os

def check_dependencies():
    """
    Check and install required Python libraries and external tools.
    Supports multiple package managers for cross-platform compatibility.
    """
    python_deps = ["impacket", "pandas", "matplotlib", "jinja2", "flask", "requests"]
    for dep in python_deps:
        try:
            __import__(dep)
        except ImportError:
            subprocess.run(["pip", "install", dep], check=True)

    required_tools = ["nmap", "crackmapexec", "enum4linux", "msfconsole"]
    for tool in required_tools:
        if not shutil.which(tool):
            if os.name == 'posix':
                if shutil.which('apt-get'):
                    subprocess.run(["apt-get", "update", "-y"], check=True)
                    subprocess.run(["apt-get", "install", "-y", tool], check=True)
                elif shutil.which('yum'):
                    subprocess.run(["yum", "install", "-y", tool], check=True)
                elif shutil.which('brew'):
                    subprocess.run(["brew", "install", tool], check=True)
            else:
                raise EnvironmentError(f"Tool {tool} not found and cannot be installed automatically.")

def validate_ip(ip):
    """Validate if the input is a valid IP address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validate_cidr(cidr):
    """Validate if the input is a valid CIDR notation."""
    try:
        ipaddress.ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False

def validate_port(port):
    """Validate if the input is a valid port number (1-65535)."""
    try:
        port = int(port)
        return 1 <= port <= 65535
    except ValueError:
        return False

def validate_username(username):
    """Validate if the username contains only alphanumeric characters and underscores."""
    return bool(re.match(r'^[a-zA-Z0-9_]+$', username))
