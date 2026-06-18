# -*- mode: python ; coding: utf-8 -*-
# Optimized build spec for Windows / Linux

from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Collect PyQt6, then strip heavy unused components to reduce bundle size.
_pyqt6_datas, _pyqt6_binaries, _pyqt6_hiddenimports = collect_all('PyQt6')

# Qt components that are never used by this app.
_QT_STRIP = [
    'WebEngine', 'WebView', 'WebChannel', 'WebSocket',
    'Qt3D', 'Quick3D', 'QtQuick', 'QtQml',
    'Bluetooth', 'Nfc', 'SerialBus', 'SerialPort',
    'Location', 'Positioning', 'Sensors',
    'Charts', 'DataVisualization',
    'Designer', 'Help', 'RemoteObjects', 'Scxml',
    'StateMachine', 'VirtualKeyboard',
]

def _keep(path):
    return not any(p.lower() in path.lower() for p in _QT_STRIP)

pyqt6_binaries      = [(s, d) for s, d in _pyqt6_binaries      if _keep(s)]
pyqt6_datas         = [(s, d) for s, d in _pyqt6_datas         if _keep(s)]
pyqt6_hiddenimports = [h       for h    in _pyqt6_hiddenimports if _keep(h)]

_PYTHON_EXCLUDES = [
    'tkinter', '_tkinter', 'PIL.ImageTk',
    'matplotlib', 'scipy', 'pandas',
    'IPython', 'jupyter', 'notebook',
    'docutils', 'sphinx',
    'PyQt6.QtWebEngineWidgets', 'PyQt6.QtWebEngineCore',
    'PyQt6.QtWebEngine', 'PyQt6.QtWebEngineQuick',
    'PyQt6.Qt3DCore', 'PyQt6.Qt3DAnimation', 'PyQt6.Qt3DExtras',
    'PyQt6.Qt3DInput', 'PyQt6.Qt3DLogic', 'PyQt6.Qt3DRender',
    'PyQt6.QtBluetooth', 'PyQt6.QtCharts', 'PyQt6.QtDataVisualization',
    'PyQt6.QtDesigner', 'PyQt6.QtHelp', 'PyQt6.QtLocation',
    'PyQt6.QtNfc', 'PyQt6.QtPositioning', 'PyQt6.QtQml',
    'PyQt6.QtQuick', 'PyQt6.QtQuick3D', 'PyQt6.QtRemoteObjects',
    'PyQt6.QtScxml', 'PyQt6.QtSensors', 'PyQt6.QtSerialBus',
    'PyQt6.QtSerialPort', 'PyQt6.QtStateMachine',
    'PyQt6.QtVirtualKeyboard', 'PyQt6.QtWebChannel', 'PyQt6.QtWebSockets',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=pyqt6_binaries,
    datas=[
        ('assets', 'assets'),
        ('config', 'config'),
        ('src', 'src'),
        ('DISTRIBUTION_README.md', '.'),
    ] + pyqt6_datas,
    hiddenimports=[
        'PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets',
        'PyQt6.sip', 'PyQt6.QtMultimedia', 'PyQt6.QtPrintSupport',
        'cv2', 'PIL', 'PIL.Image', 'PIL.ImageDraw', 'PIL.ImageFont',
        'numpy', 'yaml', 'dotenv', 'dateutil',
        'pkg_resources', 'jaraco', 'jaraco.text', 'jaraco.context',
        'jaraco.functools', 'more_itertools', 'autocommand',
        'smtplib', 'email',
        'win32print', 'win32api', 'win32con',
    ] + pyqt6_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=_PYTHON_EXCLUDES,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Photobooth',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # add 'assets/icon.ico' when available
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Photobooth',
    contents_directory='.',
)
