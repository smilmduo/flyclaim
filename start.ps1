# FlyClaim AI - Quick Start Script for Windows
# Run this after setting up environment variables in .env

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "      FlyClaim AI - Starting Application" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (!(Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run these commands first:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor White
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  pip install -r requirements.txt" -ForegroundColor White
    Write-Host ""
    exit 1
}

# Check if .env exists
if (!(Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run these commands first:" -ForegroundColor Yellow
    Write-Host "  copy .env.example .env" -ForegroundColor White
    Write-Host "  notepad .env  # Add your API keys" -ForegroundColor White
    Write-Host ""
    exit 1
}

# Check if database exists
if (!(Test-Path "flyclaim.db")) {
    Write-Host "⚠️  Database not initialized. Initializing now..." -ForegroundColor Yellow
    & ".\venv\Scripts\python.exe" backend/database/init_db.py
    Write-Host ""
}

Write-Host "✅ Starting Flask API..." -ForegroundColor Green
Write-Host ""
Write-Host "Server will run on: http://localhost:5000" -ForegroundColor White
Write-Host "Demo page: http://localhost:5000/demo" -ForegroundColor White
Write-Host ""
Write-Host "To start n8n (in another terminal):" -ForegroundColor Yellow
Write-Host "  n8n" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment and start Flask
& ".\venv\Scripts\Activate.ps1"
& ".\venv\Scripts\python.exe" backend/app.py
