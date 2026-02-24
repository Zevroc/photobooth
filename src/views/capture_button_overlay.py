"""
Photobooth Miss – Bouton HTML en overlay PyQt6
Overlay pour bouton de capture avec effets HTML/CSS/JS

Note: WebEngine est optionnel. Si indisponible, le bouton standard est utilisé.
"""

try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebEngineCore import QWebEngineScript
    from PyQt6.QtWebChannel import QWebChannel
    WEBENGINE_AVAILABLE = True
except ImportError:
    WEBENGINE_AVAILABLE = False
    # Fallback imports
    from PyQt6.QtWidgets import QPushButton, QWidget
    QWebEngineView = None
    QWebChannel = None

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QUrl, pyqtSlot, QObject, pyqtSignal
from PyQt6.QtGui import QColor


# ─────────────────────────────────────────────────────────────────────────────
# HTML du bouton Miss (identique à photobooth_overlay.py)
# ─────────────────────────────────────────────────────────────────────────────
BUTTON_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  html, body {
    width: 100%; height: 100%;
    background: transparent !important;
    overflow: hidden;
    display: flex; align-items: center; justify-content: center;
  }

  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital@1&family=Cormorant+Garamond:wght@300;400&display=swap');

  .btn-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 14px;
  }

  .crown {
    font-size: 2.2rem;
    animation: crown-float 3s ease-in-out infinite;
    filter: drop-shadow(0 0 12px rgba(212,175,55,0.9));
    user-select: none;
  }
  @keyframes crown-float {
    0%,100% { transform: translateY(0) rotate(-3deg); }
    50%      { transform: translateY(-8px) rotate(3deg); }
  }

  .photobooth-btn {
    position: relative;
    cursor: pointer;
    border: none;
    background: transparent;
    outline: none;
    -webkit-tap-highlight-color: transparent;
  }

  .btn-ring {
    position: absolute;
    inset: -18px; border-radius: 50%;
    border: 1px solid rgba(212,175,55,0.3);
    animation: ring-spin 10s linear infinite;
  }
  .btn-ring::before, .btn-ring::after {
    content: '✦'; position: absolute;
    font-size: 10px; color: #d4af37;
    top: 50%; transform: translateY(-50%);
  }
  .btn-ring::before { left: -8px; }
  .btn-ring::after  { right: -8px; }

  .btn-ring-2 {
    position: absolute;
    inset: -32px; border-radius: 50%;
    border: 1px dashed rgba(212,175,55,0.15);
    animation: ring-spin 18s linear infinite reverse;
  }
  @keyframes ring-spin { to { transform: rotate(360deg); } }

  .btn-face {
    width: 140px; height: 140px;
    border-radius: 50%;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center; gap: 6px;
    background: radial-gradient(circle at 35% 30%, #2a1a0e, #0d0008 60%, #1a0012);
    box-shadow:
      0 0 0 2px rgba(212,175,55,0.45),
      0 0 0 4px rgba(212,175,55,0.1),
      0 8px 40px rgba(0,0,0,0.8),
      inset 0 1px 0 rgba(212,175,55,0.3);
    transition: transform 0.15s ease, box-shadow 0.3s ease;
    overflow: hidden;
    position: relative;
  }
  .btn-face::before {
    content: '';
    position: absolute; inset: 0; border-radius: 50%;
    background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, transparent 50%);
    pointer-events: none;
  }
  .btn-face::after {
    content: '';
    position: absolute; inset: 0; border-radius: 50%;
    background: radial-gradient(circle, rgba(212,175,55,0.18) 0%, transparent 70%);
    opacity: 0; transition: opacity 0.3s;
  }
  .photobooth-btn:hover .btn-face {
    transform: scale(1.07);
    box-shadow:
      0 0 0 2px rgba(212,175,55,0.8),
      0 0 0 6px rgba(212,175,55,0.15),
      0 12px 50px rgba(0,0,0,0.9),
      0 0 30px rgba(212,175,55,0.25),
      inset 0 1px 0 rgba(212,175,55,0.4);
  }
  .photobooth-btn:hover .btn-face::after { opacity: 1; }
  .photobooth-btn:active .btn-face {
    transform: scale(0.95);
    animation: shutter-flash 0.35s ease;
  }
  @keyframes shutter-flash {
    30% { background: radial-gradient(circle, #fff8e7, #d4af37 30%, #0d0008 70%); }
  }

  .camera-icon {
    width: 44px; height: 44px;
    fill: none; stroke: #d4af37;
    stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round;
    filter: drop-shadow(0 0 6px rgba(212,175,55,0.6));
    transition: transform 0.3s, filter 0.3s;
    position: relative; z-index: 1;
  }
  .photobooth-btn:hover .camera-icon {
    transform: scale(1.12);
    filter: drop-shadow(0 0 14px rgba(212,175,55,1));
  }

  .btn-label {
    font-family: 'Cormorant Garamond', serif;
    font-size: 10px; font-weight: 300;
    letter-spacing: 0.28em; text-transform: uppercase;
    color: rgba(212,175,55,0.75);
    position: relative; z-index: 1;
  }

  .diamonds {
    display: flex; gap: 6px; align-items: center;
  }
  .diamond {
    width: 6px; height: 6px;
    background: #d4af37; transform: rotate(45deg); opacity: 0.35;
  }
  .diamond.center { width: 8px; height: 8px; opacity: 0.7; }

  .btn-caption {
    font-family: 'Playfair Display', serif;
    font-size: 0.9rem; font-style: italic;
    color: rgba(212,175,55,0.5);
    letter-spacing: 0.05em;
  }

  /* Flash overlay */
  .flash-overlay {
    position: fixed; inset: 0;
    background: white; opacity: 0;
    pointer-events: none; z-index: 999;
  }
  .flash-overlay.flash {
    animation: screen-flash 0.5s ease forwards;
  }
  @keyframes screen-flash {
    10% { opacity: 0.85; } 100% { opacity: 0; }
  }

  /* Burst */
  .burst-particle {
    position: fixed;
    border-radius: 50%;
    pointer-events: none;
    z-index: 100;
    opacity: 0;
    animation: burst var(--d) ease forwards;
  }
  @keyframes burst {
    0%   { transform: translate(0,0) scale(1); opacity: 1; }
    100% { transform: translate(var(--tx), var(--ty)) scale(0); opacity: 0; }
  }

  /* Sparkles */
  .sparkle {
    position: fixed;
    border-radius: 50%;
    background: #f5d47a;
    pointer-events: none;
    opacity: 0;
    animation: sp var(--dur) ease-in-out infinite;
  }
  @keyframes sp {
    0%   { transform: translateY(0) scale(0); opacity: 0; }
    30%  { opacity: 0.7; }
    100% { transform: translateY(-100px) scale(1.5); opacity: 0; }
  }
</style>
</head>
<body>

<div class="flash-overlay" id="flashOverlay"></div>

<div class="btn-wrapper">
  <div class="crown">👑</div>

  <button class="photobooth-btn" id="photoBtn" onclick="handleClick()">
    <div class="btn-ring-2"></div>
    <div class="btn-ring"></div>
    <div class="btn-face">
      <svg class="camera-icon" viewBox="0 0 24 24">
        <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
        <circle cx="12" cy="13" r="4"/>
        <circle cx="12" cy="13" r="2" stroke="rgba(212,175,55,0.5)" stroke-width="1"/>
        <circle cx="18.5" cy="10" r="1" fill="#d4af37" stroke="none"/>
      </svg>
      <span class="btn-label">Capture</span>
    </div>
  </button>

  <div class="diamonds">
    <div class="diamond"></div>
    <div class="diamond center"></div>
    <div class="diamond"></div>
  </div>
  <p class="btn-caption">Votre moment de gloire…</p>
</div>

<script>
  // Paillettes ambiantes
  function spawnSparkle() {
    const el = document.createElement('div');
    el.className = 'sparkle';
    el.style.setProperty('--dur', (2.5 + Math.random()*3)+'s');
    el.style.left   = (10 + Math.random()*80) + '%';
    el.style.top    = (30 + Math.random()*50) + '%';
    el.style.width  = el.style.height = (1+Math.random()*3)+'px';
    el.style.animationDelay = (Math.random()*2)+'s';
    document.body.appendChild(el);
    setTimeout(()=>el.remove(), 6000);
  }
  setInterval(spawnSparkle, 500);

  function handleClick() {
    // Flash
    const fl = document.getElementById('flashOverlay');
    fl.classList.remove('flash');
    void fl.offsetWidth;
    fl.classList.add('flash');

    // Burst
    const cx = window.innerWidth/2, cy = window.innerHeight/2;
    const colors = ['#d4af37','#f5d47a','#fff8e7','#e8c44a','#c0507a'];
    for (let i = 0; i < 22; i++) {
      const p = document.createElement('div');
      p.className = 'burst-particle';
      const angle = (i/22)*Math.PI*2;
      const dist  = 60 + Math.random()*90;
      p.style.left = cx+'px'; p.style.top = cy+'px';
      p.style.setProperty('--tx', Math.cos(angle)*dist+'px');
      p.style.setProperty('--ty', Math.sin(angle)*dist+'px');
      p.style.setProperty('--d', (0.4+Math.random()*0.4)+'s');
      p.style.background = colors[Math.floor(Math.random()*colors.length)];
      const s = 3+Math.random()*5;
      p.style.width = p.style.height = s+'px';
      p.style.marginLeft = p.style.marginTop = (-s/2)+'px';
      document.body.appendChild(p);
      setTimeout(()=>p.remove(), 900);
    }

    // Notifier Python
    if (window.pybridge) {
      window.pybridge.on_photo_taken();
    }
  }
</script>
</body>
</html>
"""


# ─────────────────────────────────────────────────────────────────────────────
# Bridge Python ↔ JavaScript
# ─────────────────────────────────────────────────────────────────────────────
class PyBridge(QObject):
    """Objet exposé au JS via QWebChannel."""

    photo_taken = pyqtSignal()

    @pyqtSlot()
    def on_photo_taken(self):
        """Appelé depuis JS quand le bouton est cliqué."""
        self.photo_taken.emit()


# ─────────────────────────────────────────────────────────────────────────────
# Widget overlay pour bouton de capture
# ─────────────────────────────────────────────────────────────────────────────
if WEBENGINE_AVAILABLE:
    class CaptureButtonOverlay(QWebEngineView):
        """
        Widget overlay WebEngine pour bouton de capture HTML/CSS/JS.
        Se superpose au QPushButton standard pour afficher le bouton Miss.
        """

        clicked = pyqtSignal()  # Émis quand le bouton est cliqué

        def __init__(self, parent: QWidget = None):
            super().__init__(parent)

            # ── Fond transparent ──
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            self.page().setBackgroundColor(QColor(Qt.GlobalColor.transparent))

            # ── Bridge Python ↔ JS ──
            self.bridge = PyBridge()
            self.channel = QWebChannel()
            self.channel.registerObject("pybridge", self.bridge)
            self.page().setWebChannel(self.channel)

            # Connecter le signal du bridge à notre signal clicked
            self.bridge.photo_taken.connect(self.clicked.emit)

            # ── Injecter qwebchannel.js + init du bridge ──
            html = self._inject_webchannel(BUTTON_HTML)
            self.setHtml(html, QUrl("about:blank"))

            # Taille fixe pour le bouton
            self.setFixedSize(280, 300)

        @staticmethod
        def _inject_webchannel(html: str) -> str:
            """Injecte qwebchannel.js et l'initialisation du bridge dans le HTML."""
            webchannel_init = """
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
            <script>
              document.addEventListener('DOMContentLoaded', function() {
                new QWebChannel(qt.webChannelTransport, function(channel) {
                  window.pybridge = channel.objects.pybridge;
                });
              });
            </script>
            """
            return html.replace("</head>", webchannel_init + "</head>", 1)

else:
    # Fallback: widget vide si WebEngine n'est pas disponible
    class CaptureButtonOverlay(QWidget):
        """
        Fallback widget quand WebEngine n'est pas disponible.
        Reste caché et ne fait rien (le bouton standard est utilisé).
        """

        clicked = pyqtSignal()

        def __init__(self, parent: QWidget = None):
            super().__init__(parent)
            self.setFixedSize(280, 300)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            # Fallback is not visible
            self.hide()
