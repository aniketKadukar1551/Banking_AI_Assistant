#!/bin/bash

echo "=================================="
echo "Banking AI Assistant - Quick Start"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Check if data exists
if [ ! -f "data/fee_schedule.pdf" ]; then
    echo ""
    echo "Generating data files..."
    python data_gen.py
    echo "✓ Data files generated"
else
    echo "✓ Data files already exist"
fi

# Run main demo
echo ""
echo "=================================="
echo "Starting Banking AI Assistant Demo"
echo "=================================="
echo ""
python main.py

echo ""
echo "=================================="
echo "Demo Complete!"
echo "=================================="
