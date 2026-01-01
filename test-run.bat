@echo off
chcp 65001 >nul
title Test Run - FLEX PRO

echo ===========================================
echo    Test Run - بررسی مشکلات
echo ===========================================
echo.

echo [1] بررسی Python...
python --version
if errorlevel 1 (
    echo ❌ Python یافت نشد!
    pause
    exit /b 1
)
echo ✓ Python OK
echo.

echo [2] بررسی Node.js...
node --version
if errorlevel 1 (
    echo ❌ Node.js یافت نشد!
    pause
    exit /b 1
)
echo ✓ Node.js OK
echo.

echo [3] بررسی فایل‌ها...
if not exist "package.json" (
    echo ❌ package.json یافت نشد!
    pause
    exit /b 1
)
echo ✓ package.json OK

if not exist "backend\run.py" (
    echo ❌ backend\run.py یافت نشد!
    pause
    exit /b 1
)
echo ✓ backend\run.py OK
echo.

echo [4] بررسی Backend venv...
if not exist "backend\venv" (
    echo ⚠ venv وجود ندارد
) else (
    echo ✓ venv موجود است
)
echo.

echo [5] بررسی node_modules...
if not exist "node_modules" (
    echo ⚠ node_modules وجود ندارد - باید npm install کنید
) else (
    echo ✓ node_modules موجود است
)
echo.

echo ===========================================
echo    همه بررسی‌ها انجام شد
echo ===========================================
echo.
echo برای اجرای پروژه: start-full-project.bat
echo.
pause

