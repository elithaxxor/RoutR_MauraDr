#!/bin/bash

echo "Starting setup..."

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
else
    echo "No requirements.txt found. Skipping Python dependencies."
fi

# Install Shell script dependencies (example: nmap, curl, etc.)
# Add or remove packages as needed for your project
echo "Installing common shell dependencies (edit as needed)..."
sudo apt-get update
sudo apt-get install -y nmap curl

# Install JavaScript (Node.js) dependencies
if [ -f "package.json" ]; then
    echo "Installing Node.js dependencies..."
    npm install
else
    echo "No package.json found. Skipping Node.js dependencies."
fi

echo "Setup complete!"
