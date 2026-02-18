# Build Instructions

## Overview
The Photobooth application has been successfully compiled to a standalone executable using PyInstaller.

## Compilation Results

### Build Information
- **Build Tool**: PyInstaller 6.3.0
- **Build Date**: 2026-02-18
- **Platform**: Linux (x86_64)
- **Executable**: `dist/Photobooth/Photobooth`
- **Total Size**: ~27 MB (including all dependencies)

### Distribution Structure
```
dist/Photobooth/
├── Photobooth                   # Main executable (2.6 MB)
└── _internal/                   # Dependencies and resources
    ├── DISTRIBUTION_README.md   # User guide
    ├── assets/                  # Application assets
    ├── config/                  # Configuration files
    ├── src/                     # Application source
    ├── base_library.zip         # Python standard library
    ├── lib*.so                  # System libraries
    └── [other dependencies]     # PyQt6, OpenCV, etc.
```

## How to Compile

### Prerequisites
1. Python 3.8 or higher
2. All runtime dependencies (install via `pip install -r requirements.txt`)
3. Build dependencies (install via `pip install -r requirements-build.txt`)

### Compilation Methods

#### Method 1: Using the build script (Recommended)
```bash
python build.py
```

This script will:
- Check if PyInstaller is installed
- Clean previous build artifacts
- Build the executable
- Verify the output
- Display build summary

#### Method 2: Using platform-specific scripts

**Linux/macOS:**
```bash
./build.sh
```

**Windows:**
```cmd
build.bat
```

#### Method 3: Direct PyInstaller command
```bash
pyinstaller photobooth.spec --clean
```

## Distribution

The entire `dist/Photobooth/` folder contains everything needed to run the application:

1. **Copy the entire folder**: `dist/Photobooth/`
2. **No Python required**: Users don't need Python installed
3. **Portable**: Can be run from any location
4. **Self-contained**: All dependencies are bundled

### For Users
- Run the `Photobooth` executable directly
- Read `_internal/DISTRIBUTION_README.md` for setup instructions
- Ensure assets and config folders are in the same directory as the executable

## Technical Details

### PyInstaller Configuration
The build uses `photobooth.spec` which configures:
- **One-folder bundle**: Executable + _internal folder
- **No console window**: GUI-only application
- **Asset bundling**: Includes assets/, config/, and docs/
- **Dependency collection**: Automatically bundles PyQt6, OpenCV, Pillow, etc.

### Executable Properties
- **Type**: ELF 64-bit LSB executable (Linux)
- **Architecture**: x86-64
- **Linking**: Dynamically linked
- **Dependencies**: Bundled in _internal/ folder

## Troubleshooting

### Build fails due to missing PyInstaller
```bash
pip install -r requirements-build.txt
```

### Build fails due to missing dependencies
```bash
pip install -r requirements.txt
```

### Executable doesn't run
- Ensure all files in `dist/Photobooth/` are present
- Check that `_internal/` folder is in the same directory as the executable
- Verify system libraries are compatible (Linux systems)

## Notes

- The executable is platform-specific (this build is for Linux x86_64)
- For Windows .exe, build on a Windows system
- For macOS app bundle, build on macOS
- Build artifacts (dist/, build/) are automatically gitignored
