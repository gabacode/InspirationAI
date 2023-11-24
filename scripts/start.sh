#!/bin/bash

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Please run 'make install' first"
    exit 1
fi

# Load venv
source venv/bin/activate

# Run the app
python3 src/main.py
