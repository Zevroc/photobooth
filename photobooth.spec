# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

block_cipher = None

pyqt6_datas, pyqt6_binaries, pyqt6_hiddenimports = collect_all('PyQt6')
webengine_datas, webengine_binaries, webengine_hiddenimports = collect_all('PyQt6.QtWebEngineWidgets')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=pyqt6_binaries + webengine_binaries,
    datas=[
        ('assets', 'assets'),
        ('config', 'config'),
        # Note: Including 'src' as data files to preserve package structure
        # This ensures dynamic imports and resource loading work correctly
        ('src', 'src'),
        ('DISTRIBUTION_README.md', '.'),
    ] + pyqt6_datas + webengine_datas,
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtWebEngineWidgets',
        'PyQt6.QtWebEngineCore',
        'PyQt6.QtWebChannel',
        'PyQt6.sip',
        'cv2',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'numpy',
        'msal',
        'requests',
        'yaml',
        'dotenv',
        'dateutil',
        'pkg_resources',
        'jaraco',
        'jaraco.text',
        'jaraco.context',
        'jaraco.functools',
        'more_itertools',
        'autocommand',
        'smtplib',
        'email',
        'win32print',
        'win32api',
        'win32con',
    ] + pyqt6_hiddenimports + webengine_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    console=False,  # No console window for GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one: 'assets/icon.ico'
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
)
