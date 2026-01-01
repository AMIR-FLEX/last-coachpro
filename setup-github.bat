@echo off
chcp 65001 >nul
title Setup GitHub Repository

echo ===========================================
echo    Setup GitHub Repository - FLEX PRO
echo ===========================================
echo.

echo [1/5] بررسی Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git نصب نشده است!
    echo لطفا Git را از https://git-scm.com/downloads نصب کنید
    pause
    exit /b 1
)
echo ✓ Git موجود است
echo.

echo [2/5] بررسی Repository...
if not exist ".git" (
    echo ⚠ Repository وجود ندارد. در حال ایجاد...
    git init
    echo ✓ Repository ایجاد شد
) else (
    echo ✓ Repository موجود است
)
echo.

echo [3/5] بررسی .gitignore...
if not exist ".gitignore" (
    echo ⚠ .gitignore وجود ندارد. در حال ایجاد...
    echo # Dependencies > .gitignore
    echo node_modules/ >> .gitignore
    echo backend/venv/ >> .gitignore
    echo .next/ >> .gitignore
    echo .env >> .gitignore
    echo ✓ .gitignore ایجاد شد
) else (
    echo ✓ .gitignore موجود است
)
echo.

echo [4/5] اضافه کردن فایل‌ها...
git add .
echo ✓ فایل‌ها اضافه شدند
echo.

echo [5/5] Commit...
git commit -m "Initial commit: FLEX PRO - سیستم مدیریت مربیگری ورزشی" 2>nul
if errorlevel 1 (
    git commit -m "Update: FLEX PRO - سیستم مدیریت مربیگری ورزشی"
)
echo ✓ Commit انجام شد
echo.

echo ===========================================
echo    مراحل بعدی:
echo ===========================================
echo.
echo 1. به https://github.com/new بروید
echo 2. یک Repository جدید بسازید (مثلا: flex-pro)
echo 3. سپس این دستور را اجرا کنید:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/flex-pro.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo یا اگر Repository از قبل وجود دارد:
echo.
echo    git remote set-url origin https://github.com/YOUR_USERNAME/flex-pro.git
echo    git push -u origin main
echo.
echo ===========================================
echo.
pause

