@echo off
chcp 65001 >nul
title حل مشکل Python 3.14

echo ===========================================
echo    حل مشکل Python 3.14
echo ===========================================
echo.

echo در حال بررسی نسخه Python...
python --version
echo.

python --version | findstr "3.14" >nul
if not errorlevel 1 (
    echo ⚠ Python 3.14 شناسایی شد!
    echo.
    echo این نسخه از Python با برخی کتابخانه‌ها سازگار نیست.
    echo.
    echo گزینه‌ها:
    echo 1. نصب dependencies بدون orjson (سریع)
    echo 2. مشاهده راهنمای نصب Python 3.13
    echo 3. خروج
    echo.
    set /p choice="کدام گزینه؟ (1/2/3): "
    
    if "%choice%"=="1" (
        echo.
        echo در حال نصب با requirements-fix.txt...
        cd backend
        if not exist venv (
            echo ایجاد virtual environment...
            python -m venv venv
        )
        call venv\Scripts\activate.bat
        python -m pip install --upgrade pip wheel setuptools
        pip install -r requirements-fix.txt
        if errorlevel 1 (
            echo.
            echo ❌ خطا در نصب!
            echo.
            echo توصیه: Python 3.13 نصب کنید
            echo لینک: https://www.python.org/downloads/
            pause
            exit /b 1
        )
        cd ..
        echo.
        echo ✅ نصب با موفقیت انجام شد!
        echo.
        echo نکته: orjson نصب نشد (اختیاری است - فقط برای سرعت بیشتر)
        echo پروژه بدون آن هم کار می‌کند.
        echo.
        pause
        exit /b 0
    ) else if "%choice%"=="2" (
        echo.
        echo 📖 راهنمای کامل در فایل INSTALL_PYTHON_313.md
        echo.
        echo خلاصه:
        echo 1. Python 3.13 را از لینک زیر دانلود کنید:
        echo    https://www.python.org/downloads/
        echo.
        echo 2. نصب کنید و "Add Python to PATH" را تیک بزنید
        echo.
        echo 3. سپس این دستورات را اجرا کنید:
        echo    cd backend
        echo    rmdir /s /q venv
        echo    python -m venv venv
        echo    venv\Scripts\activate.bat
        echo    pip install -r requirements.txt
        echo.
        pause
        exit /b 0
    ) else (
        exit /b 0
    )
) else (
    echo ✓ نسخه Python مناسب است!
    echo در حال نصب dependencies...
    cd backend
    if not exist venv (
        python -m venv venv
    )
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip wheel setuptools
    pip install -r requirements.txt
    cd ..
    echo.
    echo ✅ نصب با موفقیت انجام شد!
    echo.
)

pause

