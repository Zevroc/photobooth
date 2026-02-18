#!/usr/bin/env python3
"""
Quick start script for the photobooth application.
This script checks dependencies and provides guidance.
"""

import sys
import subprocess
import os


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✓ Python version: {sys.version_info.major}.{sys.version_info.minor}")
    return True


def check_dependencies():
    """Check if required dependencies are installed."""
    required = [
        'PyQt6',
        'cv2',
        'PIL',
        'numpy'
    ]
    
    missing = []
    for module in required:
        try:
            __import__(module)
            print(f"✓ {module} installed")
        except ImportError:
            missing.append(module)
            print(f"❌ {module} not installed")
    
    return missing


def create_directories():
    """Create necessary directories."""
    dirs = [
        'assets/frames',
        'assets/photos',
        'assets/temp',
        'config'
    ]
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created {directory}")


def main():
    """Main function."""
    print("=" * 60)
    print("Photobooth Application - Quick Start")
    print("=" * 60)
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    print()
    
    # Check dependencies
    print("Checking dependencies...")
    missing = check_dependencies()
    print()
    
    if missing:
        print("⚠️  Missing dependencies detected")
        print()
        print("To install dependencies, run:")
        print("  pip install -r requirements.txt")
        print()
        print("Or install them individually:")
        for dep in missing:
            print(f"  pip install {dep}")
        print()
        response = input("Would you like to install now? (y/n): ")
        if response.lower() == 'y':
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print("✓ All dependencies installed")
    print()
    
    # Create directories
    print("Creating necessary directories...")
    create_directories()
    print()
    
    print("=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Add photo frames (PNG with transparency) to 'assets/frames/'")
    print("2. Run the application: python main.py")
    print("3. Configure settings in the Admin panel")
    print()
    print("For more information, see:")
    print("- docs/INSTALLATION.md")
    print("- docs/ARCHITECTURE.md")
    print("=" * 60)


if __name__ == "__main__":
    main()
