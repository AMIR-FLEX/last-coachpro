@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title FLEX PRO - Full Project Launcher (DevOps Optimized)

echo ===========================================
echo    FLEX PRO - Full Project Launcher
echo    DevOps Optimized with Error Handling
echo ===========================================
echo.

REM ============================================
REM Step 1: Verify Python 3.11
REM ============================================
echo [1/7] Verifying Python 3.11...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.11.
    echo.
    echo Download from: https://www.python.org/downloads/release/python-31112/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

python --version | findstr "3.11" >nul
if errorlevel 1 (
    echo [WARNING] Python 3.11 not detected!
    echo.
    python --version
    echo.
    echo Please ensure Python 3.11 is the default Python.
    echo If you have multiple Python versions, use: py -3.11
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "!continue!"=="y" exit /b 1
) else (
    python --version
    echo [OK] Python 3.11 detected
)
echo.

REM ============================================
REM Step 2: Verify Node.js
REM ============================================
echo [2/7] Verifying Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found! Please install Node.js 18+.
    echo.
    echo Download from: https://nodejs.org/
    echo.
    pause
    exit /b 1
)
node --version
echo [OK] Node.js found
echo.

REM ============================================
REM Step 3: Recreate Backend Virtual Environment
REM ============================================
echo [3/7] Setting up Backend Virtual Environment...
cd backend

REM Force delete existing venv
if exist "venv" (
    echo    Deleting existing virtual environment...
    taskkill /F /IM python.exe /T >nul 2>&1
    timeout /t 1 /nobreak >nul
    rmdir /s /q venv 2>nul
    if exist "venv" (
        echo [ERROR] Could not delete venv folder!
        echo Please close all Python processes and try again.
        echo.
        pause
        cd ..
        exit /b 1
    )
    echo [OK] Old venv deleted
)

REM Create new venv with Python 3.11
echo    Creating new virtual environment with Python 3.11...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    echo.
    pause
    cd ..
    exit /b 1
)
echo [OK] Virtual environment created

REM Verify activation script exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment activation script not found!
    pause
    cd ..
    exit /b 1
)

REM Activate and upgrade pip
call venv\Scripts\activate.bat
echo    Upgrading pip, wheel, setuptools...
python -m pip install --upgrade pip wheel setuptools --quiet
if errorlevel 1 (
    echo [ERROR] Failed to upgrade pip
    pause
    cd ..
    exit /b 1
)
echo [OK] Pip upgraded
cd ..
echo.

REM ============================================
REM Step 4: Install Backend Dependencies
REM ============================================
echo [4/7] Installing Backend Dependencies...
cd backend
call venv\Scripts\activate.bat

echo    Installing from requirements.txt...
pip install --quiet -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Some dependencies failed. Checking which ones...
    pip install -r requirements.txt --no-cache-dir 2>&1 | findstr /C:"ERROR" /C:"error" /C:"Failed"
    echo.
    echo [ERROR] Backend dependency installation failed!
    echo.
    echo Troubleshooting:
    echo 1. Ensure Python 3.11 is installed correctly
    echo 2. Try running: backend\recreate-venv-python311.bat
    echo 3. Manually install: pip install -r requirements.txt
    echo.
    pause
    cd ..
    exit /b 1
)
echo [OK] Backend dependencies installed
cd ..
echo.

REM ============================================
REM Step 5: Verify Frontend package.json
REM ============================================
echo [5/7] Verifying Frontend Configuration...
if not exist "package.json" (
    echo [ERROR] package.json not found!
    pause
    exit /b 1
)
echo [OK] package.json found

if not exist ".npmrc" (
    echo    Creating .npmrc...
    echo legacy-peer-deps=true > .npmrc
    echo [OK] .npmrc created
)
echo.

REM ============================================
REM Step 6: Install Frontend Dependencies
REM ============================================
echo [6/7] Installing Frontend Dependencies...
if not exist "node_modules" (
    echo    Installing npm packages (this may take a while)...
    call npm install --legacy-peer-deps
    if errorlevel 1 (
        echo [ERROR] Frontend dependency installation failed!
        echo.
        echo Troubleshooting:
        echo 1. Delete node_modules folder: rmdir /s /q node_modules
        echo 2. Delete package-lock.json if exists
        echo 3. Run: npm cache clean --force
        echo 4. Run: npm install --legacy-peer-deps
        echo.
        pause
        exit /b 1
    )
    echo [OK] Frontend dependencies installed
) else (
    echo [OK] node_modules found (skipping installation)
)
echo.

REM ============================================
REM Step 7: Start Services
REM ============================================
echo [7/7] Starting Services...
echo.
echo ===========================================
echo    Services Starting...
echo ===========================================
echo.
echo 📍 Backend:  http://localhost:8000
echo 📍 Frontend: http://localhost:3000
echo 📍 API Docs: http://localhost:8000/docs
echo.
echo ⚠ IMPORTANT: Keep these windows open!
echo Press Ctrl+C in each window to stop the service.
echo.

REM Start Backend
echo [STARTING] Backend Server...
cd backend
start "FLEX PRO - Backend (Port 8000)" cmd /k "title FLEX PRO - Backend ^& venv\Scripts\activate.bat ^& echo Starting Backend on http://localhost:8000... ^& python run.py"
cd ..

REM Wait for backend to initialize
echo    Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Verify backend is running
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Backend health check failed, but continuing...
    echo Please check the Backend window for errors.
) else (
    echo [OK] Backend server is running
)
echo.

REM Start Frontend
echo [STARTING] Frontend Server...
start "FLEX PRO - Frontend (Port 3000)" cmd /k "title FLEX PRO - Frontend ^& cd /d %~dp0 ^& echo Starting Frontend on http://localhost:3000... ^& npm run dev"

REM Wait a bit
timeout /t 3 /nobreak >nul

echo.
echo ===========================================
echo    ✅ Services Started!
echo ===========================================
echo.
echo Two command windows have been opened:
echo   1. Backend  - Check for any errors
echo   2. Frontend - Check for any errors
echo.
echo If you see errors, please:
echo   1. Check the error messages in the windows
echo   2. Verify Python 3.11 is installed correctly
echo   3. Verify Node.js 18+ is installed correctly
echo   4. Run backend\recreate-venv-python311.bat if backend fails
echo.
echo Press any key to exit this launcher (services will continue running)...
pause >nul
