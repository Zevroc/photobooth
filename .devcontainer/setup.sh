#!/bin/bash
# Runs once when the Codespace is created.
set -e

echo "=== System dependencies ==="
sudo apt-get update -q
sudo apt-get install -y \
    xvfb x11vnc novnc \
    libgl1 libegl1 libxkbcommon0 libxcb-cursor0 libglib2.0-0

echo "=== Python dependencies ==="
pip install -r requirements.txt

echo "=== App directories ==="
mkdir -p assets/frames assets/photos assets/temp config

chmod +x start_app.sh

echo ""
echo "Setup done. Run ./start_app.sh to launch the app."
