$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

$pythonPath = Join-Path $projectRoot ".venv\Scripts\python.exe"
$backendPort = 8010
$frontendPort = 8502
$apiUrl = "http://127.0.0.1:$backendPort"

if (-not (Test-Path $pythonPath)) {
    Write-Host "Creating virtual environment..."
    $globalPython = Join-Path $env:LocalAppData "Programs\Python\Python312\python.exe"
    if (-not (Test-Path $globalPython)) {
        throw "Python 3.12 not found. Install it first, then rerun this script."
    }
    & $globalPython -m venv ".venv"
}

Write-Host "Installing or updating dependencies..."
& $pythonPath -m pip install -r "backend\requirements.txt" | Out-Null

Write-Host "Starting backend on port $backendPort..."
$backendCmd = "cd `"$projectRoot`"; .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port $backendPort"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd | Out-Null

Write-Host "Starting frontend on port $frontendPort..."
$frontendCmd = "cd `"$projectRoot`"; `$env:API_URL=`"$apiUrl`"; .\.venv\Scripts\python.exe -m streamlit run frontend_streamlit\app.py --server.headless true --server.port $frontendPort"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd | Out-Null

Start-Sleep -Seconds 3
Write-Host ""
Write-Host "Smart Plant project launched."
Write-Host "Backend docs: $apiUrl/docs"
Write-Host "Frontend:    http://localhost:$frontendPort"
Write-Host ""
Write-Host "To stop quickly, run: .\stop.ps1"
