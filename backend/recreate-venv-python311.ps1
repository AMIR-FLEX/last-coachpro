# ============================================
# Recreate Virtual Environment (Python 3.11)
# ============================================

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   Recreate Virtual Environment (Python 3.11)" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python 3.11
Write-Host "[1/4] Checking Python 3.11..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1 | Out-String
if ($pythonVersion -notmatch "Python 3\.11") {
    Write-Host "❌ Python 3.11 not detected!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Current Python version: $pythonVersion" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please ensure Python 3.11 is installed and in PATH." -ForegroundColor Yellow
    Write-Host "Download from: https://www.python.org/downloads/release/python-31112/" -ForegroundColor Cyan
    Write-Host ""
    pause
    exit 1
}
Write-Host "✓ Python 3.11 detected: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Delete existing venv
Write-Host "[2/4] Deleting existing virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "   Removing venv folder..." -ForegroundColor Cyan
    try {
        Remove-Item -Recurse -Force "venv"
        Write-Host "✓ Old venv deleted" -ForegroundColor Green
    } catch {
        Write-Host "⚠ Could not delete venv. Please close all Python processes and try again." -ForegroundColor Yellow
        Write-Host "Error: $_" -ForegroundColor Red
        pause
        exit 1
    }
} else {
    Write-Host "✓ No existing venv found" -ForegroundColor Green
}
Write-Host ""

# Create new venv
Write-Host "[3/4] Creating new virtual environment with Python 3.11..." -ForegroundColor Yellow
python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "✓ Virtual environment created" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "[4/4] Upgrading pip, wheel, and setuptools..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel setuptools
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to upgrade pip" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "✓ Pip upgraded" -ForegroundColor Green
Write-Host ""

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   Virtual Environment Ready!" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Activate: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  2. Install: pip install -r requirements.txt" -ForegroundColor White
Write-Host ""

