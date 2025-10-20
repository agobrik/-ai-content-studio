#!/bin/bash
# AI Content Studio - Linux/macOS Launcher

echo "====================================="
echo "  AI Content Studio"
echo "====================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run setup.sh first or create venv manually."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Launch application
echo "Launching AI Content Studio..."
echo ""
python src/main.py

# Deactivate virtual environment on exit
deactivate
