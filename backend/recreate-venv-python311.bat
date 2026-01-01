@echo off
chcp 65001 >nul
title Recreate Python 3.11 Virtual Environment

echo ===========================================
echo    Recreate Virtual Environment (Python 3.11)
echo ===========================================
echo.

echo [1/4] Checking Python 3.11...
python --version | findstr "3.11" >nul
if errorlevel 1 (
    echo ❌ Python 3.11 not detected!
    echo.
    echo Current Python version:
    python --version
    echo.
    echo Please ensure Python 3.11 is installed and in PATH.
    echo Download from: https://www.python.org/downloads/release/python-31112/
    echo.
    pause
    exit /b 1
)
python --version
echo ✓ Python 3.11 detected
echo.

echo [2/4] Deleting existing virtual environment...
if exist "venv" (
    echo    Removing venv folder...
    rmdir /s /q venv 2>nul
    if errorlevel 1 (
        echo ⚠ Could not delete venv. Please close all Python processes and try again.
        pause
        exit /b 1
    )
    echo ✓ Old venv deleted
) else (
    echo ✓ No existing venv found
)
echo.

echo [3/4] Creating new virtual environment with Python 3.11...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo [4/4] Upgrading pip, wheel, and setuptools...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip wheel setuptools
if errorlevel 1 (
    echo ❌ Failed to upgrade pip
    pause
    exit /b 1
)
echo ✓ Pip upgraded
echo.

echo ===========================================
echo    Virtual Environment Ready!
echo ===========================================
echo.
echo Next steps:
echo   1. Activate: venv\Scripts\activate.bat
echo   2. Install: pip install -r requirements.txt
echo.
pause

