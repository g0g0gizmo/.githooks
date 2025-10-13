# PowerShell script to create venv and install dependencies
param(
    [string]$VenvPath = ".venv"
)
if (-Not (Test-Path $VenvPath)) {
    python -m venv $VenvPath
}
$pip = Join-Path $VenvPath "Scripts\pip.exe"
if (-Not (Test-Path $pip)) {
    $pip = Join-Path $VenvPath "bin\pip"
}
if (-Not (Test-Path $pip)) {
    Write-Error "pip not found in venv."
    exit 1
}
# If requirements.txt exists, use it; else, generate from pyproject.toml
if (Test-Path "requirements.txt") {
    & $pip install -r requirements.txt
} elseif (Test-Path "pyproject.toml") {
    # Use pip to install from pyproject.toml (PEP 621, pip 23.1+)
    & $pip install .
} else {
    Write-Error "No requirements.txt or pyproject.toml found."
    exit 1
}
Write-Host "Venv ready at $VenvPath. Activate with: `n.\$VenvPath\Scripts\Activate.ps1"