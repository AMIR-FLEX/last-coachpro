@echo off
chcp 65001 >nul
title FLEX PRO - Full Project Launcher

echo ===========================================
echo    FLEX PRO - Full Project Launcher
echo ===========================================
echo.

echo [1/6] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python.
    pause
    exit /b 1
)
python --version
echo ✓ Python found
set PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1
echo.

echo [2/6] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found! Please install Node.js.
    pause
    exit /b 1
)
node --version
echo ✓ Node.js found
echo.

echo [3/6] Checking Backend Environment...
if not exist "backend\venv" (
    echo ⚠ Virtual Environment not found. Creating...
    cd backend
    python -m venv venv
    cd ..
    echo ✓ Virtual Environment created
) else (
    echo ✓ Virtual Environment found
)
echo.

echo [4/6] Installing Backend Dependencies...
cd backend
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual Environment activation script not found!
    echo    Recreating venv...
    rmdir /s /q venv 2>nul
    python -m venv venv
)
call venv\Scripts\activate.bat
set PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1
echo    Upgrading pip...
python -m pip install --upgrade pip wheel setuptools >nul 2>&1
echo    Checking Python version...
python --version | findstr "3.14" >nul
if not errorlevel 1 (
    echo ⚠ Python 3.14 detected. Using requirements-fix.txt (without orjson)...
    pip install -r requirements-fix.txt
    if errorlevel 1 (
        echo ❌ Error installing backend dependencies
        echo    Recommendation: Install Python 3.11 or 3.13
        echo    https://www.python.org/downloads/
        cd ..
        pause
        exit /b 1
    )
) else (
    echo    Installing dependencies...
    pip install --prefer-binary -r requirements.txt
    if errorlevel 1 (
        echo ⚠ Some dependencies failed. Trying requirements-fix.txt...
        pip install -r requirements-fix.txt
        if errorlevel 1 (
            echo.
            echo ❌ Error installing backend dependencies
            echo.
            echo راه‌حل: اجرای fix-python-314.bat
            echo یا نصب Python 3.13 از:
            echo https://www.python.org/downloads/
            echo.
            cd ..
            pause
            exit /b 1
        )
    )
)
cd ..
echo ✓ Backend dependencies installed
echo.

echo [5/6] Checking Frontend Dependencies...
if not exist "package.json" (
    echo ❌ package.json not found!
    pause
    exit /b 1
)
if not exist "node_modules" (
    echo ⚠ node_modules not found. Installing...
    call npm install
    if errorlevel 1 (
        echo ❌ Error installing frontend dependencies
        pause
        exit /b 1
    )
    echo ✓ Frontend dependencies installed
) else (
    echo ✓ Frontend dependencies found
)
echo.

echo [6/6] Database will be auto-created on backend start...
echo.

echo ===========================================
echo    Starting Services...
echo ===========================================
echo.
echo 📍 Backend: http://localhost:8000
echo 📍 Frontend: http://localhost:3000
echo 📍 API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo.

echo 🚀 Starting Backend...
cd backend
start "FLEX PRO - Backend" cmd /k "venv\Scripts\activate.bat && python run.py"
cd ..

timeout /t 3 /nobreak >nul

echo 🚀 Starting Frontend...
start "FLEX PRO - Frontend" cmd /k "cd /d %~dp0 && npm run dev"

echo.
echo ✅ Project started successfully!
echo 📝 Two command windows opened for Backend and Frontend.
echo.
echo To stop all services: Close the windows or press Ctrl+C.
echo.
pause
