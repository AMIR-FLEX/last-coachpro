@echo off
chcp 65001 >nul
title Push to GitHub

echo ===========================================
echo    Push to GitHub - FLEX PRO
echo ===========================================
echo.

echo [1/4] بررسی تغییرات...
git status
echo.

echo [2/4] اضافه کردن فایل‌های جدید...
git add .
echo ✓ فایل‌ها اضافه شدند
echo.

echo [3/4] Commit تغییرات...
set /p commit_msg="پیام Commit را وارد کنید (یا Enter برای استفاده از پیام پیش‌فرض): "
if "%commit_msg%"=="" set commit_msg=Update: FLEX PRO - سیستم مدیریت مربیگری ورزشی
git commit -m "%commit_msg%"
echo ✓ Commit انجام شد
echo.

echo [4/4] Push به GitHub...
set /p branch="نام Branch (default: main): "
if "%branch%"=="" set branch=main
git push origin %branch%
if errorlevel 1 (
    echo.
    echo ⚠ خطا در Push!
    echo.
    echo اگر Repository برای اولین بار است:
    echo   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
    echo   git branch -M main
    echo   git push -u origin main
    echo.
    pause
    exit /b 1
)
echo.
echo ✅ با موفقیت به GitHub Push شد!
echo.
pause

