# آپدیت فایل‌ها در GitHub
# PowerShell Script

$ErrorActionPreference = "Stop"

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  آپدیت فایل‌ها در GitHub" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# تغییر به دایرکتوری پروژه
Set-Location $PSScriptRoot

# بررسی اینکه آیا git initialized است
if (-not (Test-Path ".git")) {
    Write-Host "⚠️  دایرکتوری Git پیدا نشد!" -ForegroundColor Yellow
    Write-Host "در حال ایجاد repository جدید..." -ForegroundColor Yellow
    git init
    Write-Host ""
}

# نمایش وضعیت فعلی
Write-Host "📊 وضعیت فعلی Git:" -ForegroundColor Blue
git status --short
Write-Host ""

# افزودن تمام فایل‌ها
Write-Host "➕ در حال افزودن تمام فایل‌ها..." -ForegroundColor Green
git add .
Write-Host "✓ فایل‌ها اضافه شدند" -ForegroundColor Green
Write-Host ""

# دریافت پیام commit
$commitMessage = Read-Host "💬 پیام commit را وارد کنید (یا Enter برای پیام پیش‌فرض)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Update project files - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
}

# Commit کردن تغییرات
Write-Host ""
Write-Host "💾 در حال commit کردن..." -ForegroundColor Blue
try {
    git commit -m $commitMessage
    Write-Host "✓ Commit با موفقیت انجام شد" -ForegroundColor Green
} catch {
    Write-Host "⚠️  خطا در commit - ممکن است تغییری برای commit وجود نداشته باشد" -ForegroundColor Yellow
    Write-Host "برای ادامه Enter را بزنید..." -ForegroundColor Yellow
    Read-Host
    exit 1
}
Write-Host ""

# نمایش remote repository
Write-Host "🔍 بررسی remote repository..." -ForegroundColor Blue
git remote -v
Write-Host ""

# Push کردن به GitHub
Write-Host "🚀 در حال push کردن به GitHub..." -ForegroundColor Magenta
$pushed = $false

# تلاش برای push به master
try {
    git push origin master 2>&1 | Out-Null
    $pushed = $true
} catch {
    # تلاش برای push به main
    try {
        git push origin main 2>&1 | Out-Null
        $pushed = $true
    } catch {
        $pushed = $false
    }
}

if (-not $pushed) {
    Write-Host ""
    Write-Host "⚠️  خطا در push - لطفاً remote repository را بررسی کنید:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. اگر remote تنظیم نشده، با دستور زیر تنظیم کنید:" -ForegroundColor Yellow
    Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git" -ForegroundColor White
    Write-Host ""
    Write-Host "2. یا نام branch را بررسی کنید (master یا main):" -ForegroundColor Yellow
    Write-Host "   git branch" -ForegroundColor White
    Write-Host ""
    Write-Host "برای ادامه Enter را بزنید..." -ForegroundColor Yellow
    Read-Host
    exit 1
}

Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "✅ همه فایل‌ها با موفقیت در GitHub آپدیت شدند!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "برای بستن Enter را بزنید..." -ForegroundColor Gray
Read-Host

