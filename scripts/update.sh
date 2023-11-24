#!/bin/bash

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Please run 'make install' first"
    exit 1
fi

# Load venv
source venv/bin/activate

# Updating dependencies
echo "Updating dependencies..."
pip install -r requirements.txt

# Close
echo "Done."
exit 0
