Write-Host "Starting FlyClaim AI - Backend & Frontend..." -ForegroundColor Cyan

# Start Backend
Write-Host "Starting Backend (Flask)..." -ForegroundColor Green
Start-Process python -ArgumentList "backend/app.py" -NoNewWindow

# Wait a moment
Start-Sleep -Seconds 2

# Start Frontend
Write-Host "Starting Frontend (Vite)..." -ForegroundColor Green
Set-Location frontend
Start-Process npm -ArgumentList "run dev" -NoNewWindow
