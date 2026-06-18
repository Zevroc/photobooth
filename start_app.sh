#!/bin/bash
# Launch Photobooth in a virtual display exposed in the browser via noVNC.
#
# Usage: ./start_app.sh
# Then open port 6080 in the Codespaces "Ports" panel.

DISPLAY_NUM=99
VNC_PORT=5900
NOVNC_PORT=6080

# ---- virtual display ----
echo "[1/3] Starting virtual display (:${DISPLAY_NUM}) ..."
pkill Xvfb 2>/dev/null || true
Xvfb :${DISPLAY_NUM} -screen 0 1280x800x24 -nolisten tcp &
export DISPLAY=:${DISPLAY_NUM}
sleep 1

# ---- VNC server ----
echo "[2/3] Starting VNC server (port ${VNC_PORT}) ..."
pkill x11vnc 2>/dev/null || true
x11vnc -display :${DISPLAY_NUM} -nopw -forever -shared \
       -rfbport ${VNC_PORT} -bg -o /tmp/x11vnc.log
sleep 1

# ---- noVNC — browser access ----
echo "[3/3] Starting noVNC (port ${NOVNC_PORT}) ..."
pkill websockify 2>/dev/null || true
nohup /usr/share/novnc/utils/novnc_proxy \
    --listen ${NOVNC_PORT} \
    --vnc localhost:${VNC_PORT} \
    &>/tmp/novnc.log &
sleep 1

echo ""
echo "================================================"
echo "  Open port ${NOVNC_PORT} in the Codespaces"
echo "  Ports panel  →  click the globe icon"
echo "  Then click \"Connect\" in the noVNC page"
echo "================================================"
echo ""

python main.py
