# ============================================
# Push to GitHub - FLEX PRO
# ============================================

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   Push to GitHub - FLEX PRO" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# بررسی Git
Write-Host "[1/5] بررسی Git..." -ForegroundColor Yellow
$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitInstalled) {
    Write-Host "❌ Git نصب نشده است!" -ForegroundColor Red
    Write-Host "لطفا Git را از https://git-scm.com/downloads نصب کنید" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Git موجود است" -ForegroundColor Green
Write-Host ""

# بررسی Repository
Write-Host "[2/5] بررسی Repository..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    Write-Host "⚠ Repository وجود ندارد. در حال ایجاد..." -ForegroundColor Yellow
    git init
    Write-Host "✓ Repository ایجاد شد" -ForegroundColor Green
} else {
    Write-Host "✓ Repository موجود است" -ForegroundColor Green
}
Write-Host ""

# بررسی .gitignore
Write-Host "[3/5] بررسی .gitignore..." -ForegroundColor Yellow
if (-not (Test-Path ".gitignore")) {
    Write-Host "⚠ .gitignore وجود ندارد. در حال ایجاد..." -ForegroundColor Yellow
    @"
# Dependencies
node_modules/
/.pnp
.pnp.js

# Testing
/coverage

# Next.js
/.next/
/out/

# Production
/build

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env*.local
.env

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts

# Python
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
venv/
env/
ENV/
backend/venv/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Database
*.db
*.sqlite
*.sqlite3
backend/flexpro.db

# Logs
*.log
logs/
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "✓ .gitignore ایجاد شد" -ForegroundColor Green
} else {
    Write-Host "✓ .gitignore موجود است" -ForegroundColor Green
}
Write-Host ""

# اضافه کردن فایل‌ها
Write-Host "[4/5] اضافه کردن فایل‌ها..." -ForegroundColor Yellow
git add .
Write-Host "✓ فایل‌ها اضافه شدند" -ForegroundColor Green
Write-Host ""

# Commit
Write-Host "[5/5] Commit..." -ForegroundColor Yellow
$commitMsg = Read-Host "پیام Commit را وارد کنید (یا Enter برای استفاده از پیام پیش‌فرض)"
if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "Update: FLEX PRO - سیستم مدیریت مربیگری ورزشی"
}
git commit -m $commitMsg
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠ خطا در Commit (ممکن است تغییری وجود نداشته باشد)" -ForegroundColor Yellow
}
Write-Host "✓ Commit انجام شد" -ForegroundColor Green
Write-Host ""

# بررسی Remote
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   Push به GitHub" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

$remoteUrl = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($remoteUrl)) {
    Write-Host "⚠ Remote Repository تنظیم نشده است!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "لطفا ابتدا Repository را در GitHub بسازید:" -ForegroundColor Cyan
    Write-Host "1. به https://github.com/new بروید" -ForegroundColor White
    Write-Host "2. یک Repository جدید بسازید" -ForegroundColor White
    Write-Host "3. سپس این دستور را اجرا کنید:" -ForegroundColor White
    Write-Host ""
    Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git" -ForegroundColor Green
    Write-Host "   git branch -M main" -ForegroundColor Green
    Write-Host "   git push -u origin main" -ForegroundColor Green
    Write-Host ""
    Write-Host "یا اگر Repository از قبل وجود دارد:" -ForegroundColor White
    Write-Host "   git remote set-url origin https://github.com/YOUR_USERNAME/REPO_NAME.git" -ForegroundColor Green
    Write-Host ""
    
    $setupNow = Read-Host "آیا می‌خواهید الان Remote را تنظیم کنید? (y/n)"
    if ($setupNow -eq "y" -or $setupNow -eq "Y") {
        $repoUrl = Read-Host "URL Repository را وارد کنید (مثلا: https://github.com/username/repo.git)"
        if (-not [string]::IsNullOrWhiteSpace($repoUrl)) {
            git remote add origin $repoUrl 2>$null
            if ($LASTEXITCODE -ne 0) {
                git remote set-url origin $repoUrl
            }
            Write-Host "✓ Remote تنظیم شد" -ForegroundColor Green
            
            # Set branch to main
            git branch -M main 2>$null
            
            # Push
            Write-Host ""
            Write-Host "در حال Push..." -ForegroundColor Yellow
            git push -u origin main
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ با موفقیت به GitHub Push شد!" -ForegroundColor Green
            } else {
                Write-Host "❌ خطا در Push!" -ForegroundColor Red
            }
        }
    }
} else {
    Write-Host "✓ Remote Repository: $remoteUrl" -ForegroundColor Green
    Write-Host ""
    
    $branch = Read-Host "نام Branch (default: main)"
    if ([string]::IsNullOrWhiteSpace($branch)) {
        $branch = "main"
    }
    
    Write-Host "در حال Push..." -ForegroundColor Yellow
    git push origin $branch
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ با موفقیت به GitHub Push شد!" -ForegroundColor Green
    } else {
        Write-Host "❌ خطا در Push!" -ForegroundColor Red
        Write-Host "ممکن است نیاز به تنظیم Branch باشد:" -ForegroundColor Yellow
        Write-Host "   git branch -M main" -ForegroundColor White
        Write-Host "   git push -u origin main" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

