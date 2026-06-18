"""
Visual smoke test: navigate through the main screens and save a screenshot of each.

Usage:
    QT_QPA_PLATFORM=offscreen python test_smoke.py

Outputs PNG files to screenshots/ (one per screen).
"""
import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_LOGGING_RULES", "*.debug=false;qt.qpa.*=false")

for _d in ("assets/frames", "assets/photos", "assets/temp", "config", "screenshots"):
    os.makedirs(_d, exist_ok=True)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

sys.argv = ["photobooth"]
app = QApplication(sys.argv)
app.setStyle("Fusion")

from main import PhotoboothApp, APP_STYLE  # noqa: E402

app.setStyleSheet(APP_STYLE)
window = PhotoboothApp()
window.resize(1280, 800)
window.show()


def _grab(name: str):
    path = f"screenshots/{name}.png"
    ok = window.grab().save(path)
    status = "OK" if ok else "FAILED"
    print(f"  [{status}] {path}")
    if not ok:
        sys.exit(1)


# Each tuple: (delay_ms, navigate_fn, screenshot_name)
_STEPS = [
    (300,  window.show_capture,  "01_capture_screen"),
    (900,  window.show_home,     "02_home_screen"),
    (1500, window.show_admin,    "03_admin_screen"),
    (2100, app.quit,             None),
]

for _ms, _fn, _name in _STEPS:
    def _make(_fn=_fn, _name=_name):
        def _step():
            _fn()
            if _name:
                app.processEvents()   # flush pending paint events
                _grab(_name)
        return _step
    QTimer.singleShot(_ms, _make())

print("Starting app — taking screenshots of each screen...")
sys.exit(app.exec())
