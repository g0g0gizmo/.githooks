Write-Host "Checking Git Hooks Dependencies..." -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[SUCCESS] Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found" -ForegroundColor Red
}

# Check virtual environment
if (Test-Path "C:\Users\g0g0g\Projects\.githooks\venv") {
    Write-Host "[SUCCESS] Virtual environment exists" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Virtual environment not found" -ForegroundColor Yellow
}

# Check dotenvx
try {
    $dotenvxVersion = dotenvx --version 2>&1
    Write-Host "[SUCCESS] dotenvx: $dotenvxVersion" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] dotenvx not found" -ForegroundColor Yellow
}

# Check Maven
try {
    $mvnVersion = mvn --version 2>&1 | Select-Object -First 1
    Write-Host "[SUCCESS] Maven: $mvnVersion" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] Maven not found" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Press Enter to continue"
