Write-Host "🚀 Installing All Dependencies" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""

# Backend
Write-Host "📦 Backend Dependencies..." -ForegroundColor Yellow
Set-Location backend

if (Test-Path "venv") {
    Write-Host "Virtual environment exists, activating..."
} else {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Backend installation failed" -ForegroundColor Red
    exit 1
}

deactivate
Set-Location ..

# Frontend
Write-Host ""
Write-Host "📦 Frontend Dependencies..." -ForegroundColor Yellow
Set-Location frontend-web

if (Test-Path "node_modules") {
    Write-Host "node_modules exists, updating..."
    npm update
} else {
    Write-Host "Installing npm packages..."
    npm install
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend installation failed" -ForegroundColor Red
    exit 1
}

Set-Location ..

# Desktop
Write-Host ""
Write-Host "📦 Desktop App Dependencies..." -ForegroundColor Yellow
Set-Location desktop-app

if (Test-Path "venv") {
    Write-Host "Virtual environment exists, activating..."
} else {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r desktop_requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Desktop app dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Desktop app installation failed" -ForegroundColor Red
    exit 1
}

deactivate
Set-Location ..

Write-Host ""
Write-Host "==============================" -ForegroundColor Cyan
Write-Host "🎉 All Dependencies Installed!" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Cyan