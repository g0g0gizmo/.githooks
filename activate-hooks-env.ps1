# Activate the git hooks virtual environment
$VenvDir = "C:\Users\g0g0g\Projects\.githooks\venv"
$activateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
} else {
    $env:PATH = "$(Join-Path $VenvDir 'Scripts');$env:PATH"
}
Write-Host ""
Write-Host "[SUCCESS] Git Hooks virtual environment activated!" -ForegroundColor Green
Write-Host "To deactivate, run: deactivate" -ForegroundColor Blue
Write-Host ""
