#!/bin/bash
# Install Python dependencies before running tests
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Simple test runner
python3 -m unittest discover -s tests -v
