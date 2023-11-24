#!/bin/bash

delimiter="=============================================="

# If the venv folder exists, remove it
if [ -d "venv" ]; then
    echo "$delimiter"
    echo "Removing existing venv directory..."
    rm -r venv
fi

# Create venv
echo "$delimiter"
echo "Creating virtual environment..."
python3 -m venv venv

# Load venv
echo "$delimiter"
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "$delimiter"
echo "Installing dependencies..."
pip install -r requirements.txt

# Echo instructions
echo "$delimiter"
echo "To run the app, execute the following command:"
echo "'make start'"
echo "$delimiter"
exit 0
