#!/usr/bin/env pwsh
# ==============================================================================
# Git Hooks Installer - PowerShell Wrapper
# ==============================================================================
# This script is a simple wrapper that calls the Python install.py script
#
# Usage: .\install.ps1 [-RepoPath <path>] [-Global] [-Force] [-SkipDeps]
#
# Examples:
#   .\install.ps1                           - Install in current directory
#   .\install.ps1 -RepoPath "C:\my\project" - Install in specific repository
#   .\install.ps1 -Global                   - Install globally
#   .\install.ps1 -Force                    - Force reinstall
# ==============================================================================

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$RepoPath = '',

    [Parameter(Mandatory = $false)]
    [switch]$Global,

    [Parameter(Mandatory = $false)]
    [switch]$Force,

    [Parameter(Mandatory = $false)]
    [switch]$SkipDeps
)

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$InstallPy = Join-Path $ScriptDir 'install.py'

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[INFO] Found Python: $pythonVersion" -ForegroundColor Blue
}
catch {
    Write-Host '[ERROR] Python is not installed or not in PATH' -ForegroundColor Red
    Write-Host 'Please install Python 3.9+ from https://python.org' -ForegroundColor Red
    Read-Host 'Press Enter to exit'
    exit 1
}

# Check if install.py exists
if (-not (Test-Path $InstallPy)) {
    Write-Host "[ERROR] install.py not found at $InstallPy" -ForegroundColor Red
    Read-Host 'Press Enter to exit'
    exit 1
}

# Build arguments for Python script
$args = @()

if ($RepoPath) {
    $args += '--repo-path'
    $args += $RepoPath
}

if ($Global) {
    $args += '--global'
}

if ($Force) {
    $args += '--force'
}

if ($SkipDeps) {
    $args += '--skip-deps'
}

# Run the Python installer
Write-Host "Running: python '$InstallPy' $($args -join ' ')" -ForegroundColor Cyan
Write-Host ''

try {
    & python $InstallPy @args
    $exitCode = $LASTEXITCODE
}
catch {
    Write-Host ''
    Write-Host "[ERROR] Installation failed: $_" -ForegroundColor Red
    Read-Host 'Press Enter to exit'
    exit 1
}

if ($exitCode -ne 0) {
    Write-Host ''
    Write-Host "[ERROR] Installation failed with exit code $exitCode" -ForegroundColor Red
    Read-Host 'Press Enter to exit'
    exit $exitCode
}

Write-Host ''
Read-Host 'Press Enter to exit'
exit 0
