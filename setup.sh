#!/bin/bash

echo "Starting setup..."

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    if command -v pip3 >/dev/null 2>&1; then
        pip3 install -r requirements.txt
    elif command -v pip >/dev/null 2>&1; then
        pip install -r requirements.txt
    else
        echo "pip not found. Please install Python dependencies manually."
    fi
else
    echo "No requirements.txt found. Skipping Python dependencies."
fi

# Install Shell script dependencies (example: nmap, curl, etc.)
# Add or remove packages as needed for your project
echo "Installing common shell dependencies (edit as needed)..."
if command -v brew >/dev/null 2>&1; then
    brew update
    brew install nmap curl
elif command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y nmap curl
elif command -v yum >/dev/null 2>&1; then
    sudo yum install -y nmap curl
else
    echo "Package manager not found. Please install nmap and curl manually."
fi

# Install JavaScript (Node.js) dependencies
if [ -f "package.json" ]; then
    echo "Installing Node.js dependencies..."
    npm install
else
    echo "No package.json found. Skipping Node.js dependencies."
fi

echo "Setup complete!"
