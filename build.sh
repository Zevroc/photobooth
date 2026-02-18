#!/bin/bash
# Photobooth Build Script for Linux/macOS
# This script automates the build process

echo "================================================================"
echo "Photobooth Application - Build Script"
echo "================================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Step 1/3: Installing build dependencies..."
echo ""
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo ""

echo "Step 2/3: Building executable..."
echo ""
python3 build.py
if [ $? -ne 0 ]; then
    echo "ERROR: Build failed"
    exit 1
fi
echo ""

echo "Step 3/3: Build complete!"
echo ""
echo "================================================================"
echo "The executable is ready in: dist/Photobooth/Photobooth"
echo "================================================================"
echo ""
