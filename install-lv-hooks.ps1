<#
Installs LabVIEW Git Hooks (https://gitlab.com/felipe_public/lv-git-hooks)
Prereqs:
- LabVIEW installed (LV2020+ recommended)
- g-cli available on PATH (LV Venv Tools / G CLI)

Usage:
  pwsh ./install-lv-hooks.ps1 [-LvOnly]

This will install pre-commit/commit-msg shims that call LV Git Hooks per .lv-git-hooks-config.json
#>
param(
  [switch]$LvOnly
)

Write-Host "Installing LabVIEW Git Hooks..."

$config = Join-Path $PSScriptRoot ".lv-git-hooks-config.json"
if (-not (Test-Path $config)) {
  Write-Error ".lv-git-hooks-config.json not found in repo root: $PSScriptRoot"
  exit 1
}

# Verify g-cli exists
$gcli = Get-Command g-cli -ErrorAction SilentlyContinue
if (-not $gcli) {
  Write-Error "g-cli not found. Install LV Venv Tools / G CLI and ensure it's on PATH."
  Write-Host "Docs: https://gitlab.com/felipe_public/lv-git-hooks"
  exit 1
}

$cliArgs = @('git-hooks','--','install')
if ($LvOnly) { $cliArgs += '--lv-only' }

Write-Host "Running: g-cli $($cliArgs -join ' ')" -ForegroundColor Cyan

Push-Location $PSScriptRoot
try {
  & g-cli @cliArgs
  if ($LASTEXITCODE -ne 0) { throw "g-cli git-hooks install failed with code $LASTEXITCODE" }
  Write-Host "LabVIEW Git Hooks installed." -ForegroundColor Green
}
finally { Pop-Location }

exit 0
