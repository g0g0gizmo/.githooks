Write-Host 'Checking Git Hooks Dependencies...' -ForegroundColor Cyan
Write-Host '===================================' -ForegroundColor Cyan
Write-Host ''

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[SUCCESS] Python: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host '[ERROR] Python not found' -ForegroundColor Red
}

# Check Python packages
try {
    $pipList = pip list --format=freeze 2>&1 | Select-String -Pattern 'gitpython|click|colorama'
    if ($pipList) {
        Write-Host '[SUCCESS] Required Python packages installed' -ForegroundColor Green
    }
    else {
        Write-Host '[WARNING] Some required packages may be missing. Run: pip install -r requirements.txt' -ForegroundColor Yellow
    }
}
catch {
    Write-Host '[WARNING] Could not verify Python packages' -ForegroundColor Yellow
}

# Check dotenvx
try {
    $dotenvxVersion = dotenvx --version 2>&1
    Write-Host "[SUCCESS] dotenvx: $dotenvxVersion" -ForegroundColor Green
}
catch {
    Write-Host '[WARNING] dotenvx not found' -ForegroundColor Yellow
}

# Check Maven
try {
    $mvnVersion = mvn --version 2>&1 | Select-Object -First 1
    Write-Host "[SUCCESS] Maven: $mvnVersion" -ForegroundColor Green
}
catch {
    Write-Host '[WARNING] Maven not found' -ForegroundColor Yellow
}

Write-Host ''
Read-Host 'Press Enter to continue'
