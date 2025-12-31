@echo off
chcp 65001 >nul
echo ====================================
echo   آپدیت فایل‌ها در GitHub
echo ====================================
echo.

REM تغییر به دایرکتوری پروژه
cd /d "%~dp0"

REM بررسی اینکه آیا git initialized است
if not exist ".git" (
    echo ⚠️  دایرکتوری Git پیدا نشد!
    echo در حال ایجاد repository جدید...
    git init
    echo.
)

REM نمایش وضعیت فعلی
echo 📊 وضعیت فعلی Git:
git status --short
echo.

REM افزودن تمام فایل‌ها
echo ➕ در حال افزودن تمام فایل‌ها...
git add .
echo ✓ فایل‌ها اضافه شدند
echo.

REM دریافت پیام commit (یا استفاده از پیام پیش‌فرض)
set /p commit_message="💬 پیام commit را وارد کنید (یا Enter برای پیام پیش‌فرض): "
if "%commit_message%"=="" set commit_message=Update project files - %date% %time%

REM Commit کردن تغییرات
echo.
echo 💾 در حال commit کردن...
git commit -m "%commit_message%"
if %errorlevel% neq 0 (
    echo ⚠️  خطا در commit - ممکن است تغییری برای commit وجود نداشته باشد
    pause
    exit /b 1
)
echo ✓ Commit با موفقیت انجام شد
echo.

REM نمایش remote repository
echo 🔍 بررسی remote repository...
git remote -v
echo.

REM تشخیص نام branch فعلی
echo 🔍 تشخیص branch فعلی...
for /f "tokens=2" %%b in ('git branch --show-current 2^>nul') do set current_branch=%%b
if "%current_branch%"=="" (
    for /f "tokens=2" %%b in ('git rev-parse --abbrev-ref HEAD 2^>nul') do set current_branch=%%b
)
if "%current_branch%"=="" set current_branch=master

REM Push کردن به GitHub
echo 🚀 در حال push کردن به GitHub (branch: %current_branch%)...
git push origin %current_branch% 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  خطا در push - لطفاً remote repository را بررسی کنید:
    echo.
    echo 1. اگر remote تنظیم نشده، با دستور زیر تنظیم کنید:
    echo    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
    echo.
    echo 2. یا نام branch و remote را بررسی کنید:
    echo    git branch
    echo    git remote -v
    echo.
    pause
    exit /b 1
)

echo.
echo ====================================
echo ✅ همه فایل‌ها با موفقیت در GitHub آپدیت شدند!
echo ====================================
echo.
pause

