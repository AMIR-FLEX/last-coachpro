# ============================================
# FLEX PRO - Full Project Launcher
# ============================================
# اسکریپت اجرای کامل پروژه (Backend + Frontend)
# اجرا: .\start-full-project.ps1

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   FLEX PRO - Full Project Launcher" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# بررسی وجود Python
Write-Host "[1/6] بررسی Python..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "❌ Python یافت نشد! لطفا Python را نصب کنید." -ForegroundColor Red
    exit 1
}
$pythonVersion = python --version 2>&1 | Out-String
Write-Host "✓ Python پیدا شد: $pythonVersion" -ForegroundColor Green

# بررسی نسخه Python (باید 3.8 تا 3.13 باشد)
$versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
if ($versionMatch) {
    $majorVersion = [int]$matches[1]
    $minorVersion = [int]$matches[2]
    if ($majorVersion -eq 3 -and $minorVersion -gt 13) {
        Write-Host "⚠ هشدار: Python 3.14 یا بالاتر شناسایی شد!" -ForegroundColor Yellow
        Write-Host "   برخی کتابخانه‌ها ممکن است کار نکنند. Python 3.11 یا 3.13 توصیه می‌شود." -ForegroundColor Yellow
        Write-Host "   در حال تنظیم متغیرهای محیطی برای حل مشکل..." -ForegroundColor Yellow
        $env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY = "1"
    }
}
Write-Host ""

# بررسی وجود Node.js
Write-Host "[2/6] بررسی Node.js..." -ForegroundColor Yellow
$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node) {
    Write-Host "❌ Node.js یافت نشد! لطفا Node.js را نصب کنید." -ForegroundColor Red
    exit 1
}
Write-Host "✓ Node.js پیدا شد: $($node.Version)" -ForegroundColor Green
Write-Host ""

# بررسی وجود virtual environment
Write-Host "[3/6] بررسی Backend Environment..." -ForegroundColor Yellow
$venvPath = "backend\venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "⚠ Virtual Environment وجود ندارد. در حال ایجاد..." -ForegroundColor Yellow
    Set-Location backend
    python -m venv venv
    Set-Location ..
    Write-Host "✓ Virtual Environment ایجاد شد" -ForegroundColor Green
}
Write-Host "✓ Virtual Environment پیدا شد" -ForegroundColor Green
Write-Host ""

# فعال‌سازی virtual environment و نصب dependencies
Write-Host "[4/6] نصب Dependencies Backend..." -ForegroundColor Yellow
$activateScript = "backend\venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
    Set-Location backend
    
    # تنظیم متغیرهای محیطی برای Python 3.14+
    $env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY = "1"
    
    # آپگرید pip
    Write-Host "   آپگرید pip..." -ForegroundColor Cyan
    python -m pip install --upgrade pip wheel setuptools
    
    # نصب dependencies با retry و استفاده از binary wheels
    Write-Host "   نصب dependencies..." -ForegroundColor Cyan
    pip install --upgrade pip wheel setuptools 2>$null
    
    # بررسی نسخه Python
    $pythonVer = python --version 2>&1 | Out-String
    if ($pythonVer -match "Python 3\.14") {
        Write-Host "⚠ Python 3.14 شناسایی شد. استفاده از requirements-fix.txt (بدون orjson)..." -ForegroundColor Yellow
        pip install -r requirements-fix.txt
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ خطا در نصب dependencies Backend" -ForegroundColor Red
            Write-Host ""
            Write-Host "راه‌حل: اجرای fix-python-314.bat" -ForegroundColor Yellow
            Write-Host "یا نصب Python 3.13 از: https://www.python.org/downloads/" -ForegroundColor Cyan
            Write-Host ""
            $fixScript = Join-Path $PWD "fix-python-314.bat"
            if (Test-Path $fixScript) {
                Start-Process $fixScript
            }
            Set-Location ..
            exit 1
        }
    } else {
        pip install -r requirements.txt --prefer-binary
        if ($LASTEXITCODE -ne 0) {
            Write-Host "⚠ خطا در نصب برخی dependencies. تلاش با requirements-fix.txt..." -ForegroundColor Yellow
            pip install -r requirements-fix.txt
            if ($LASTEXITCODE -ne 0) {
                Write-Host "❌ خطا در نصب dependencies Backend" -ForegroundColor Red
                Write-Host "   لطفا Python 3.11 یا 3.13 نصب کنید:" -ForegroundColor Yellow
                Write-Host "   https://www.python.org/downloads/" -ForegroundColor Cyan
                Set-Location ..
                exit 1
            }
        }
    }
    Set-Location ..
    Write-Host "✓ Dependencies Backend نصب شدند" -ForegroundColor Green
} else {
    Write-Host "❌ فایل activate یافت نشد!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# بررسی و نصب Dependencies Frontend
Write-Host "[5/6] بررسی Dependencies Frontend..." -ForegroundColor Yellow
if (-not (Test-Path "node_modules")) {
    Write-Host "⚠ node_modules وجود ندارد. در حال نصب..." -ForegroundColor Yellow
    # بررسی اینکه آیا package-nextjs.json وجود دارد (Next.js) یا package.json (Vite)
    if (Test-Path "package-nextjs.json") {
        Write-Host "📦 استفاده از Next.js..." -ForegroundColor Cyan
        Copy-Item "package-nextjs.json" "package.json" -Force
    }
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ خطا در نصب dependencies Frontend" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Dependencies Frontend نصب شدند" -ForegroundColor Green
} else {
    Write-Host "✓ Dependencies Frontend موجود هستند" -ForegroundColor Green
}
Write-Host ""

# بررسی دیتابیس
Write-Host "[6/6] بررسی دیتابیس..." -ForegroundColor Yellow
if (-not (Test-Path "backend\flexpro.db")) {
    Write-Host "⚠ دیتابیس وجود ندارد. در حال ایجاد..." -ForegroundColor Yellow
    Set-Location backend
    & .\venv\Scripts\python.exe -c "from app.db.init_db import init_db; init_db()"
    Set-Location ..
    Write-Host "✓ دیتابیس ایجاد شد" -ForegroundColor Green
} else {
    Write-Host "✓ دیتابیس موجود است" -ForegroundColor Green
}
Write-Host ""

# اجرای Backend و Frontend
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   در حال راه‌اندازی سرویس‌ها..." -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Backend: http://localhost:8000" -ForegroundColor Green
Write-Host "📍 Frontend: http://localhost:3000" -ForegroundColor Green
Write-Host "📍 API Docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "برای توقف: Ctrl+C" -ForegroundColor Yellow
Write-Host ""

# شروع Backend در پنجره جدید
Write-Host "🚀 راه‌اندازی Backend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList @"
    -NoExit -Command `
    `$Host.UI.RawUI.WindowTitle = 'FLEX PRO - Backend'; `
    Set-Location '$PWD\backend'; `
    .\venv\Scripts\Activate.ps1; `
    python run.py
"@

# کمی صبر برای راه‌اندازی Backend
Start-Sleep -Seconds 3

# شروع Frontend در پنجره جدید
Write-Host "🚀 راه‌اندازی Frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList @"
    -NoExit -Command `
    `$Host.UI.RawUI.WindowTitle = 'FLEX PRO - Frontend'; `
    Set-Location '$PWD'; `
    if (Test-Path 'package-nextjs.json') { Copy-Item 'package-nextjs.json' 'package.json' -Force }; `
    npm run dev
"@

Write-Host ""
Write-Host "✅ پروژه با موفقیت راه‌اندازی شد!" -ForegroundColor Green
Write-Host "📝 دو پنجره PowerShell برای Backend و Frontend باز شده است." -ForegroundColor Yellow
Write-Host ""
Write-Host "برای بستن همه سرویس‌ها: پنجره‌ها را ببندید یا Ctrl+C بزنید." -ForegroundColor Yellow
Write-Host ""

