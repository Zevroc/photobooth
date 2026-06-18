"""
Smoke test: launch the app in offscreen mode, capture a screenshot, exit.

Usage:
    QT_QPA_PLATFORM=offscreen python test_smoke.py

The screenshot is saved to screenshots/smoke_test.png.
"""
import os
import sys

# Force offscreen rendering before any Qt import
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_LOGGING_RULES", "*.debug=false;qt.qpa.*=false")

# Ensure required directories exist (app expects them on first run)
for _d in ("assets/frames", "assets/photos", "assets/temp", "config", "screenshots"):
    os.makedirs(_d, exist_ok=True)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

sys.argv = ["photobooth"]
app = QApplication(sys.argv)
app.setStyle("Fusion")

from main import PhotoboothApp, APP_STYLE  # noqa: E402  (needs QApplication first)

app.setStyleSheet(APP_STYLE)
window = PhotoboothApp()
window.resize(1280, 800)
window.show()


def _capture_and_quit():
    pixmap = window.grab()
    out = "screenshots/smoke_test.png"
    if pixmap.save(out):
        print(f"Screenshot saved → {out}")
    else:
        print("ERROR: could not save screenshot", file=sys.stderr)
        sys.exit(1)
    app.quit()


# Allow 3 s for the UI to fully render before capturing
QTimer.singleShot(3000, _capture_and_quit)

sys.exit(app.exec())
