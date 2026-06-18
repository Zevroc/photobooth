#!/usr/bin/env python3
"""
Build script for creating Photobooth executable.
This script automates the process of building the application using PyInstaller.
"""

import sys
import subprocess
import os
import shutil
import platform


def clean_build_directories():
    """Clean previous build artifacts."""
    print("[INFO] Cleaning previous build artifacts...")
    directories = ['build', 'dist']
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"   Removed {directory}/")
    print("[OK] Build directories cleaned\n")


def check_dependencies():
    """Check if PyInstaller is installed."""
    print("[INFO] Checking build dependencies...")
    try:
        import PyInstaller
        print(f"[OK] PyInstaller {PyInstaller.__version__} is installed\n")
        return True
    except ImportError:
        print("[ERROR] PyInstaller is not installed")
        print("\nTo install PyInstaller, run:")
        print("  pip install pyinstaller\n")
        return False


def get_spec_file():
    """Return the appropriate PyInstaller spec file for the current platform."""
    if platform.system() == "Darwin":
        return "photobooth_macos.spec"
    return "photobooth.spec"


def build_executable():
    """Build the executable using PyInstaller."""
    spec_file = get_spec_file()
    print(f"[INFO] Building executable using {spec_file}...")
    print("   This may take a few minutes...\n")

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'PyInstaller', spec_file, '--clean'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("[OK] Build completed successfully!\n")
            return True
        else:
            print("[ERROR] Build failed!")
            print("\nError output:")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"[ERROR] Error during build: {e}")
        return False


def verify_build():
    """Verify that the output was created."""
    print("[INFO] Verifying build output...")

    system = platform.system()

    if system == "Darwin":
        app_path = os.path.join('dist', 'Photobooth.app')
        if os.path.exists(app_path):
            size_mb = sum(
                os.path.getsize(os.path.join(dp, f))
                for dp, _, files in os.walk(app_path)
                for f in files
            ) / (1024 * 1024)
            print(f"[OK] App bundle created: {app_path}")
            print(f"  Size: {size_mb:.1f} MB\n")
            return True
        print(f"[ERROR] App bundle not found at {app_path}\n")
        return False

    exe_extension = '.exe' if system == 'Windows' else ''
    exe_path = os.path.join('dist', 'Photobooth', f'Photobooth{exe_extension}')

    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"[OK] Executable created: {exe_path}")
        print(f"  Size: {size_mb:.1f} MB\n")
        return True

    print(f"[ERROR] Executable not found at {exe_path}\n")
    return False


def main():
    """Main build process."""
    system = platform.system()

    print("=" * 60)
    print("Photobooth Application - Build Script")
    print("=" * 60)
    print()
    print(f"Platform: {system} ({platform.machine()})\n")

    if not check_dependencies():
        sys.exit(1)

    clean_build_directories()

    if not build_executable():
        sys.exit(1)

    if not verify_build():
        sys.exit(1)

    print("=" * 60)
    print("[OK] Build completed successfully!")
    print("=" * 60)
    print()

    if system == "Darwin":
        print("The app bundle is located at:")
        print("  dist/Photobooth.app")
        print()
        print("To distribute the application:")
        print("1. Copy dist/Photobooth.app to the target Mac")
        print("2. Or drag it to /Applications to install system-wide")
        print("3. On first launch, right-click > Open to bypass Gatekeeper")
        print("   (unless the app is signed with an Apple Developer ID)")
    elif system == "Windows":
        print("The executable is located at:")
        print("  dist\\Photobooth\\Photobooth.exe")
        print()
        print("To distribute the application:")
        print("1. Copy the entire 'dist/Photobooth' folder")
        print("2. The folder contains all necessary files and dependencies")
        print("3. Users can run Photobooth.exe directly (no Python needed)")
    else:
        print("The executable is located at:")
        print("  dist/Photobooth/Photobooth")
        print()
        print("To distribute the application:")
        print("1. Copy the entire 'dist/Photobooth' folder")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
