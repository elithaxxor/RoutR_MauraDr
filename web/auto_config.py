import os
import subprocess

# Define the configuration content
config_ini_content = """
[database]
path = smb_enum.db

[logging]
level = DEBUG
log_to_console = true

[network]
default_cidr = 192.168.1.0/24

[server]
host = 0.0.0.0
port = 5000
debug = true

[jwt]
secret_key = your-secret-key
"""

config_yaml_content = """
database:
  path: smb_enum.db

logging:
  level: DEBUG
  log_to_console: true

network:
  default_cidr: 192.168.1.0/24

server:
  host: "0.0.0.0"
  port: 5000
  debug: true

jwt:
  secret_key: "your-secret-key"
"""

# Paths for configuration files
base_dir = os.path.join(os.getcwd(), "web")
config_ini_path = os.path.join(base_dir, "config.ini")
config_yaml_path = os.path.join(base_dir, "config.yaml")

# Function to create a file
def create_file(path, content):
    with open(path, "w") as file:
        file.write(content)
    print(f"Created: {path}")

# Ensure the base directory exists
os.makedirs(base_dir, exist_ok=True)

# Create the configuration files
create_file(config_ini_path, config_ini_content)
create_file(config_yaml_path, config_yaml_content)

# Install Python dependencies from requirements.txt (if it exists)
requirements_path = os.path.join(os.getcwd(), "requirements.txt")
if os.path.exists(requirements_path):
    subprocess.run(["pip", "install", "-r", requirements_path], check=True)
    print(f"Installed dependencies from: {requirements_path}")
else:
    print("requirements.txt not found. Skipping Python dependencies installation.")
