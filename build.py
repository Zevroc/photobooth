#!/usr/bin/env python3
"""
Build script for creating Photobooth executable.
This script automates the process of building the application using PyInstaller.
"""

import sys
import subprocess
import os
import shutil


def clean_build_directories():
    """Clean previous build artifacts."""
    print("🧹 Cleaning previous build artifacts...")
    directories = ['build', 'dist']
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"   Removed {directory}/")
    print("✓ Build directories cleaned\n")


def check_dependencies():
    """Check if PyInstaller is installed."""
    print("📦 Checking build dependencies...")
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} is installed\n")
        return True
    except ImportError:
        print("❌ PyInstaller is not installed")
        print("\nTo install PyInstaller, run:")
        print("  pip install pyinstaller\n")
        return False


def build_executable():
    """Build the executable using PyInstaller."""
    print("🔨 Building executable...")
    print("   This may take a few minutes...\n")
    
    try:
        # Run PyInstaller with the spec file
        result = subprocess.run(
            [sys.executable, '-m', 'PyInstaller', 'photobooth.spec', '--clean'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ Build completed successfully!\n")
            return True
        else:
            print("❌ Build failed!")
            print("\nError output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error during build: {e}")
        return False


def verify_build():
    """Verify that the executable was created."""
    print("🔍 Verifying build output...")
    
    exe_path = os.path.join('dist', 'Photobooth', 'Photobooth.exe')
    
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"✓ Executable created: {exe_path}")
        print(f"  Size: {size_mb:.1f} MB\n")
        return True
    else:
        print(f"❌ Executable not found at {exe_path}\n")
        return False


def main():
    """Main build process."""
    print("=" * 60)
    print("Photobooth Application - Build Script")
    print("=" * 60)
    print()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Clean previous builds
    clean_build_directories()
    
    # Build executable
    if not build_executable():
        sys.exit(1)
    
    # Verify build
    if not verify_build():
        sys.exit(1)
    
    # Success message
    print("=" * 60)
    print("🎉 Build completed successfully!")
    print("=" * 60)
    print()
    print("The executable is located at:")
    print("  dist/Photobooth/Photobooth.exe")
    print()
    print("Distribution files included:")
    print("  - Photobooth.exe (main application)")
    print("  - DISTRIBUTION_README.md (user guide)")
    print("  - assets/ (frames, photos, temp)")
    print("  - config/ (configuration)")
    print("  - _internal/ (dependencies)")
    print()
    print("To distribute the application:")
    print("1. Copy the entire 'dist/Photobooth' folder")
    print("2. The folder contains all necessary files and dependencies")
    print("3. Users can run Photobooth.exe directly (no Python needed)")
    print()
    print("Note: Users should read DISTRIBUTION_README.md for setup")
    print("=" * 60)


if __name__ == "__main__":
    main()
