# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for macOS — produces a .app bundle

from PyInstaller.utils.hooks import collect_all

block_cipher = None

pyqt6_datas, pyqt6_binaries, pyqt6_hiddenimports = collect_all('PyQt6')

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
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.sip',
        'cv2',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'numpy',
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
    ] + pyqt6_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['win32print', 'win32api', 'win32con', 'win32ui'],
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
    argv_emulation=True,  # required for macOS Open With / file association
    target_arch=None,     # None = native arch; set to 'universal2' for fat binary
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # replace with 'assets/icon.icns' when available
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

app = BUNDLE(
    coll,
    name='Photobooth.app',
    icon=None,  # replace with 'assets/icon.icns' when available
    bundle_identifier='com.zevroc.photobooth',
    info_plist={
        'CFBundleName': 'Photobooth',
        'CFBundleDisplayName': 'Photobooth',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'NSCameraUsageDescription': 'Photobooth requires camera access to capture photos.',
        'NSMicrophoneUsageDescription': 'Photobooth may use audio feedback during capture.',
        'LSMinimumSystemVersion': '10.13.0',
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
    },
)
