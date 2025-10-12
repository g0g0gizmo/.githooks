# ==============================================================================
# Git Hooks Complete Installation Script for Windows (PowerShell)
# ==============================================================================
# This script:
# 1. Sets up a Python virtual environment
# 2. Installs all required dependencies (Python packages and system tools)
# 3. Installs git hooks to a repository or globally
#
# Usage: .\install-all.ps1 [-RepoPath <path>] [-Global]
#   -RepoPath: Path to git repository (optional, current dir if not specified)
#   -Global: Install hooks globally for all repositories
#
# Examples:
#   .\install-all.ps1                                - Install in current directory
#   .\install-all.ps1 -RepoPath "C:\my\project"      - Install in specific repository
#   .\install-all.ps1 -Global                       - Install globally
# ==============================================================================

param(
    [string]$RepoPath = (Get-Location).Path,
    [switch]$Global
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "  Git Hooks Complete Installation Script" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvDir = Join-Path $ScriptDir "venv"
$RequirementsFile = Join-Path $ScriptDir "requirements.txt"

# Resolve full path
$RepoPath = Resolve-Path $RepoPath -ErrorAction SilentlyContinue
if (-not $RepoPath) {
    $RepoPath = (Get-Location).Path
}

Write-Host "Step 1: Setting up Python Virtual Environment" -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Yellow
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[SUCCESS] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.6+ from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path $VenvDir)) {
    Write-Host "[INFO] Creating Python virtual environment..." -ForegroundColor Blue
    try {
        python -m venv $VenvDir
        Write-Host "[SUCCESS] Virtual environment created" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Failed to create virtual environment: $_" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "[INFO] Virtual environment already exists" -ForegroundColor Blue
}

# Activate virtual environment
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Blue
$activateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
} else {
    Write-Host "[WARNING] PowerShell activation script not found, using batch version" -ForegroundColor Yellow
    $env:PATH = "$(Join-Path $VenvDir 'Scripts');$env:PATH"
}

# Upgrade pip
Write-Host "[INFO] Upgrading pip..." -ForegroundColor Blue
try {
    python -m pip install --upgrade pip | Out-Null
    Write-Host "[SUCCESS] Pip upgraded" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] Failed to upgrade pip: $_" -ForegroundColor Yellow
}

# Install Python dependencies
if (Test-Path $RequirementsFile) {
    Write-Host "[INFO] Installing Python dependencies..." -ForegroundColor Blue
    try {
        pip install -r $RequirementsFile
        Write-Host "[SUCCESS] Python dependencies installed" -ForegroundColor Green
    } catch {
        Write-Host "[WARNING] Some Python dependencies failed to install: $_" -ForegroundColor Yellow
    }
} else {
    Write-Host "[WARNING] No requirements.txt found, skipping Python dependencies" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 2: Checking System Dependencies" -ForegroundColor Yellow
Write-Host "====================================" -ForegroundColor Yellow
Write-Host ""

# Check for dotenvx
try {
    $dotenvxVersion = dotenvx --version 2>&1
    Write-Host "[SUCCESS] dotenvx is available: $dotenvxVersion" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] dotenvx not found" -ForegroundColor Yellow
    Write-Host "          Install from: https://dotenvx.com/docs/install" -ForegroundColor Yellow
    Write-Host "          Windows: iwr https://dotenvx.sh/windows.ps1 | iex" -ForegroundColor Yellow
}

# Check for Maven
try {
    $mvnVersion = mvn --version 2>&1 | Select-Object -First 1
    Write-Host "[SUCCESS] Maven is available: $mvnVersion" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] Maven not found" -ForegroundColor Yellow
    Write-Host "          Some hooks may not work without Maven" -ForegroundColor Yellow
    Write-Host "          Install from: https://maven.apache.org/install.html" -ForegroundColor Yellow
}

# Check for Git
try {
    $gitVersion = git --version 2>&1
    Write-Host "[SUCCESS] Git is available: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git is not installed or not in PATH" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 3: Installing Git Hooks" -ForegroundColor Yellow
Write-Host "=============================" -ForegroundColor Yellow
Write-Host ""

if ($Global) {
    Write-Host "[INFO] Installing hooks globally..." -ForegroundColor Blue
    Install-GlobalHooks
} else {
    Write-Host "[INFO] Installing hooks to repository: $RepoPath" -ForegroundColor Blue
    Install-LocalHooks
}

Write-Host ""
Write-Host "Step 4: Creating Helper Scripts" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow
Write-Host ""

# Create activation script
$activateScript = Join-Path $ScriptDir "activate-hooks-env.ps1"
@"
# Activate the git hooks virtual environment
`$VenvDir = "$VenvDir"
`$activateScript = Join-Path `$VenvDir "Scripts\Activate.ps1"
if (Test-Path `$activateScript) {
    & `$activateScript
} else {
    `$env:PATH = "`$(Join-Path `$VenvDir 'Scripts');`$env:PATH"
}
Write-Host ""
Write-Host "[SUCCESS] Git Hooks virtual environment activated!" -ForegroundColor Green
Write-Host "To deactivate, run: deactivate" -ForegroundColor Blue
Write-Host ""
"@ | Out-File -FilePath $activateScript -Encoding UTF8

Write-Host "[SUCCESS] Created activation script: activate-hooks-env.ps1" -ForegroundColor Green

# Create dependency checker script
$checkScript = Join-Path $ScriptDir "check-dependencies.ps1"
@"
Write-Host "Checking Git Hooks Dependencies..." -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    `$pythonVersion = python --version 2>&1
    Write-Host "[SUCCESS] Python: `$pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found" -ForegroundColor Red
}

# Check virtual environment
if (Test-Path "$VenvDir") {
    Write-Host "[SUCCESS] Virtual environment exists" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Virtual environment not found" -ForegroundColor Yellow
}

# Check dotenvx
try {
    `$dotenvxVersion = dotenvx --version 2>&1
    Write-Host "[SUCCESS] dotenvx: `$dotenvxVersion" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] dotenvx not found" -ForegroundColor Yellow
}

# Check Maven
try {
    `$mvnVersion = mvn --version 2>&1 | Select-Object -First 1
    Write-Host "[SUCCESS] Maven: `$mvnVersion" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] Maven not found" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Press Enter to continue"
"@ | Out-File -FilePath $checkScript -Encoding UTF8

Write-Host "[SUCCESS] Created dependency checker: check-dependencies.ps1" -ForegroundColor Green

Write-Host ""
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  Installation Complete!" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Virtual environment: $VenvDir" -ForegroundColor Blue
Write-Host "Activation script:   activate-hooks-env.ps1" -ForegroundColor Blue
Write-Host "Dependency checker:  check-dependencies.ps1" -ForegroundColor Blue
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Run '.\activate-hooks-env.ps1' to activate the Python environment" -ForegroundColor White
Write-Host "2. Run '.\check-dependencies.ps1' to verify all dependencies" -ForegroundColor White
Write-Host "3. Install any missing system dependencies mentioned above" -ForegroundColor White
Write-Host ""
if ($Global) {
    Write-Host "Your hooks are now installed globally for all Git repositories." -ForegroundColor Green
} else {
    Write-Host "Your hooks are now installed in: $RepoPath" -ForegroundColor Green
}
Write-Host ""
Read-Host "Press Enter to exit"

# ==============================================================================
# Function to install hooks globally
# ==============================================================================
function Install-GlobalHooks {
    $defaultHooksDir = Join-Path $env:USERPROFILE ".git-hooks"
    Write-Host "[INFO] Global hooks directory: $defaultHooksDir" -ForegroundColor Blue

    # Create the global hooks directory if it doesn't exist
    if (-not (Test-Path $defaultHooksDir)) {
        New-Item -ItemType Directory -Path $defaultHooksDir -Force | Out-Null
        Write-Host "[SUCCESS] Created global hooks directory" -ForegroundColor Green
    }

    # Configure Git to use the global hooks directory
    try {
        git config --global core.hooksPath $defaultHooksDir
        Write-Host "[SUCCESS] Configured Git to use global hooks directory" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Failed to configure Git global hooks path: $_" -ForegroundColor Red
        return
    }

    # Copy all hooks to global directory
    Write-Host "[INFO] Copying hooks to global directory..." -ForegroundColor Blue
    $hookDirs = Get-ChildItem -Path $ScriptDir -Directory | Where-Object { 
        Test-Path (Join-Path $_.FullName "README.md") 
    }

    foreach ($hookDir in $hookDirs) {
        $hookType = $hookDir.Name
        Write-Host "[INFO] Processing $hookType hooks..." -ForegroundColor Blue
        
        $hookFiles = Get-ChildItem -Path $hookDir.FullName -Filter "*.hook"
        foreach ($hookFile in $hookFiles) {
            $hookName = $hookFile.BaseName -replace '\.hook$', ''
            $destPath = Join-Path $defaultHooksDir $hookType
            
            try {
                Copy-Item $hookFile.FullName $destPath -Force
                Write-Host "[SUCCESS] Installed $hookType/$hookName" -ForegroundColor Green
            } catch {
                Write-Host "[WARNING] Failed to install $hookType/$hookName: ${_}" -ForegroundColor Yellow
            }
        }
    }
}

# ==============================================================================
# Function to install hooks locally
# ==============================================================================
function Install-LocalHooks {
    # Check if repository exists and has .git directory
    $gitDir = Join-Path $RepoPath ".git"
    if (-not (Test-Path $gitDir)) {
        Write-Host "[ERROR] $RepoPath is not a Git repository" -ForegroundColor Red
        return
    }

    $hooksDir = Join-Path $gitDir "hooks"

    # Create hooks directory if it doesn't exist
    if (-not (Test-Path $hooksDir)) {
        New-Item -ItemType Directory -Path $hooksDir -Force | Out-Null
    }

    Write-Host "[INFO] Available hook types:" -ForegroundColor Blue
    $hookDirs = Get-ChildItem -Path $ScriptDir -Directory | Where-Object { 
        Test-Path (Join-Path $_.FullName "README.md") 
    }

    $count = 0
    $hookTypes = @{}
    foreach ($hookDir in $hookDirs) {
        $count++
        $hookName = $hookDir.Name
        Write-Host "  $count. $hookName" -ForegroundColor White
        $hookTypes[$count] = $hookName
    }

    Write-Host ""
    $selection = Read-Host "Select hook types to install (e.g., 1,3,5) or 'all' for all hooks"

    if ($selection -eq "all") {
        # Install all hooks
        foreach ($hookDir in $hookDirs) {
            Copy-HookType $hookDir.FullName $hooksDir
        }
    } else {
        # Install selected hooks
        $selections = $selection -split ',' | ForEach-Object { $_.Trim() }
        foreach ($sel in $selections) {
            if ($hookTypes.ContainsKey([int]$sel)) {
                $hookTypeName = $hookTypes[[int]$sel]
                $hookTypeDir = Join-Path $ScriptDir $hookTypeName
                Copy-HookType $hookTypeDir $hooksDir
            }
        }
    }
}

# ==============================================================================
# Function to copy a specific hook type
# ==============================================================================
function Copy-HookType {
    param(
        [string]$SourceDir,
        [string]$HooksDir
    )
    
    $hookType = Split-Path -Leaf $SourceDir
    Write-Host "[INFO] Installing $hookType hooks..." -ForegroundColor Blue
    
    $hookFiles = Get-ChildItem -Path $SourceDir -Filter "*.hook"
    foreach ($hookFile in $hookFiles) {
        $hookName = $hookFile.BaseName -replace '\.hook$', ''
        $destPath = Join-Path $HooksDir $hookType
        
        # Check if this is a Python script and update shebang
        $content = Get-Content $hookFile.FullName -Raw
        if ($content -match '#!.*python') {
            # Update shebang to use virtual environment
            $pythonExe = Join-Path $VenvDir "Scripts\python.exe"
            $updatedContent = $content -replace '#!.*python.*', "#!$pythonExe"
            $updatedContent | Out-File -FilePath $destPath -Encoding UTF8 -NoNewline
            Write-Host "[SUCCESS] Installed $hookType/$hookName (updated for venv)" -ForegroundColor Green
        } else {
            Copy-Item $hookFile.FullName $destPath -Force
            Write-Host "[SUCCESS] Installed $hookType/$hookName" -ForegroundColor Green
        }
    }
}