@echo off
REM Photobooth Build Script for Windows
REM This batch file automates the build process

echo ================================================================
echo Photobooth Application - Build Script
echo ================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Step 1/2: Installing dependencies...
echo.
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-build.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo Step 2/2: Building executable...
echo.
python build.py
if %errorlevel% neq 0 (
    echo ERROR: Build failed
    pause
    exit /b 1
)
echo.

echo ================================================================
echo Build complete!
echo.
echo ================================================================
echo The executable is ready in: dist\Photobooth\Photobooth.exe
echo ================================================================
echo.
pause
