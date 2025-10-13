@echo off
setlocal enabledelayedexpansion

REM ==============================================================================
REM Git Hooks Complete Installation Script for Windows
REM ==============================================================================
REM This script:
REM 1. Sets up a Python virtual environment
REM 2. Installs all required dependencies (Python packages and system tools)
REM 3. Installs git hooks to a repository or globally
REM
REM Usage: install-all.bat [repo-path] [global]
REM   repo-path: Path to git repository (optional, current dir if not specified)
REM   global: Use "global" to install hooks globally for all repositories
REM
REM Examples:
REM   install-all.bat                          - Install in current directory
REM   install-all.bat "C:\my\project"          - Install in specific repository
REM   install-all.bat . global                - Install globally
REM ==============================================================================

echo.
echo =====================================================================
echo  Git Hooks Complete Installation Script
echo =====================================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%venv"
set "REQUIREMENTS_FILE=%SCRIPT_DIR%requirements.txt"
set "REPO_PATH=%~1"
set "GLOBAL_FLAG=%~2"

REM Default to current directory if no repo path specified
if "%REPO_PATH%"=="" set "REPO_PATH=%CD%"

REM Resolve full path
for %%i in ("%REPO_PATH%") do set "REPO_PATH=%%~fi"

echo Step 1: Setting up Python Virtual Environment
echo ===============================================

REM Check if Python is available
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://python.org
    pause
    exit /b 1
)

REM Always recreate virtual environment
if exist "%VENV_DIR%" (
    echo [INFO] Removing existing Python virtual environment...
    rmdir /s /q "%VENV_DIR%"
)
echo [INFO] Creating Python virtual environment...
python -m venv "%VENV_DIR%"
if !errorlevel! neq 0 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment created

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install Python dependencies
if exist "%REQUIREMENTS_FILE%" (
    echo [INFO] Installing Python dependencies...
    pip install -r "%REQUIREMENTS_FILE%"
    if !errorlevel! equ 0 (
        echo [SUCCESS] Python dependencies installed
    ) else (
        echo [WARNING] Some Python dependencies failed to install
    )
) else (
    echo [WARNING] No requirements.txt found, skipping Python dependencies
)

echo.
echo Step 2: Checking System Dependencies
echo ====================================
REM Detect platform (Git Bash, PowerShell, or CMD)
set "PLATFORM=cmd"
ver | findstr /i "Microsoft" >nul 2>&1 && (
    set "PLATFORM=cmd"
)
where bash >nul 2>&1 && (
    bash -c "echo $0" 2>nul | findstr /i "bash" >nul 2>&1 && set "PLATFORM=gitbash"
)
where pwsh >nul 2>&1 && (
    set "PLATFORM=powershell"
)

REM Check for dotenvx
dotenvx --version >nul 2>&1
if !errorlevel! equ 0 (
    echo [SUCCESS] dotenvx is available
) else (
    echo [WARNING] dotenvx not found
    echo           Please install dotenvx manually for your shell:
    if /i "%PLATFORM%"=="gitbash" (
        echo           - For Git Bash: curl -sfS https://dotenvx.sh ^| sh
    ) else (
        if /i "%PLATFORM%"=="powershell" (
            echo           - For PowerShell: irm https://dotenvx.sh ^| iex
        ) else (
            echo           - For CMD: Use PowerShell or Git Bash to install dotenvx
        )
    )
    echo           See: https://dotenvx.com/docs/install
)

REM Check for Maven
mvn --version >nul 2>&1
if !errorlevel! equ 0 (
    echo [SUCCESS] Maven is available
) else (
    echo [WARNING] Maven not found
    echo           Please install Maven manually:
    if /i "%PLATFORM%"=="gitbash" (
        echo           - For Git Bash: Use SDKMAN or download from https://maven.apache.org/install.html
    ) else (
        if /i "%PLATFORM%"=="powershell" (
            echo           - For PowerShell: choco install maven -y
        ) else (
            echo           - For CMD: Download from https://maven.apache.org/install.html or use Chocolatey
        )
    )
    echo           See: https://maven.apache.org/install.html
)

REM Check for Git
git --version >nul 2>&1
if !errorlevel! equ 0 (
    echo [SUCCESS] Git is available
) else (
    echo [ERROR] Git is not installed or not in PATH
    echo           Please install Git manually:
    echo           - Download: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo.
echo Step 3: Installing Git Hooks
echo =============================

if /i "%GLOBAL_FLAG%"=="global" (
    echo [INFO] Installing hooks globally...
    call :install_global_hooks
) else (
    echo [INFO] Installing hooks to repository: %REPO_PATH%
    call :install_local_hooks
)

echo.
echo Step 4: Creating Helper Scripts
echo ===============================

REM Create activation script
set "ACTIVATE_SCRIPT=%SCRIPT_DIR%activate-hooks-env.bat"
(
    echo @echo off
    echo REM Activate the git hooks virtual environment
    echo call "%VENV_DIR%\Scripts\activate.bat"
    echo echo.
    echo echo [SUCCESS] Git Hooks virtual environment activated!
    echo echo To deactivate, run: deactivate
    echo echo.
) > "%ACTIVATE_SCRIPT%"

echo [SUCCESS] Created activation script: activate-hooks-env.bat

REM Create requirements check script
set "CHECK_SCRIPT=%SCRIPT_DIR%check-dependencies.bat"
(
    echo @echo off
    echo echo Checking Git Hooks Dependencies...
    echo echo ===================================
    echo.
    echo REM Check Python
    echo python --version ^>nul 2^>^&1
    echo if ^^!errorlevel^^! equ 0 ^(
    echo     python --version
    echo ^) else ^(
    echo     echo [ERROR] Python not found
    echo ^)
    echo.
    echo REM Check virtual environment
    echo if exist "%VENV_DIR%" ^(
    echo     echo [SUCCESS] Virtual environment exists
    echo ^) else ^(
    echo     echo [WARNING] Virtual environment not found
    echo ^)
    echo.
    echo REM Check dotenvx
    echo dotenvx --version ^>nul 2^>^&1
    echo if ^^!errorlevel^^! equ 0 ^(
    echo     echo [SUCCESS] dotenvx is available
    echo ^) else ^(
    echo     echo [WARNING] dotenvx not found
    echo ^)
    echo.
    echo REM Check Maven
    echo mvn --version ^>nul 2^>^&1
    echo if ^^!errorlevel^^! equ 0 ^(
    echo     echo [SUCCESS] Maven is available
    echo ^) else ^(
    echo     echo [WARNING] Maven not found
    echo ^)
    echo.
    echo pause
) > "%CHECK_SCRIPT%"

echo [SUCCESS] Created dependency checker: check-dependencies.bat

echo.
echo =================================================================
echo  Installation Complete!
echo =================================================================
echo.
echo Virtual environment: %VENV_DIR%
echo Activation script:   activate-hooks-env.bat
echo Dependency checker:  check-dependencies.bat
echo.
echo Next steps:
echo 1. Run 'activate-hooks-env.bat' to activate the Python environment
echo 2. Run 'check-dependencies.bat' to verify all dependencies
echo 3. Install any missing system dependencies mentioned above
echo.
if /i "%GLOBAL_FLAG%"=="global" (
    echo Your hooks are now installed globally for all Git repositories.
) else (
    echo Your hooks are now installed in: %REPO_PATH%
)
echo.
pause
goto :eof

REM ==============================================================================
REM Function to install hooks globally
REM ==============================================================================
:install_global_hooks
set "DEFAULT_HOOKS_DIR=%USERPROFILE%\.git-hooks"
echo [INFO] Global hooks directory: %DEFAULT_HOOKS_DIR%

REM Create the global hooks directory if it doesn't exist
if not exist "%DEFAULT_HOOKS_DIR%" (
    mkdir "%DEFAULT_HOOKS_DIR%"
    echo [SUCCESS] Created global hooks directory
)

REM Configure Git to use the global hooks directory
git config --global core.hooksPath "%DEFAULT_HOOKS_DIR%"
if !errorlevel! equ 0 (
    echo [SUCCESS] Configured Git to use global hooks directory
) else (
    echo [ERROR] Failed to configure Git global hooks path
    goto :eof
)

REM Copy all hooks to global directory
echo [INFO] Copying hooks to global directory...
for /d %%i in ("%SCRIPT_DIR%*") do (
    if exist "%%i\README.md" (
        set "hooktype=%%~ni"
        echo [INFO] Processing !hooktype! hooks...
        
        for %%j in ("%%i\*.hook") do (
            set "hookfile=%%~nj"
            set "hookname=!hookfile:.hook=!"
            copy "%%j" "%DEFAULT_HOOKS_DIR%\!hooktype!" >nul 2>&1
            if !errorlevel! equ 0 (
                echo [SUCCESS] Installed !hooktype!/!hookname!
            )
        )
    )
)
goto :eof

REM ==============================================================================
REM Function to install hooks locally
REM ==============================================================================
:install_local_hooks
REM Check if repository exists and has .git directory
if not exist "%REPO_PATH%\.git" (
    echo [ERROR] %REPO_PATH% is not a Git repository
    goto :eof
)

set "HOOKS_DIR=%REPO_PATH%\.git\hooks"

REM Create hooks directory if it doesn't exist
if not exist "%HOOKS_DIR%" mkdir "%HOOKS_DIR%"

echo [INFO] Available hook types:
set /a count=0
for /d %%i in ("%SCRIPT_DIR%*") do (
    if exist "%%i\README.md" (
        set "hookname=%%~ni"
        if not "!hookname!"=="" (
            set /a count+=1
            echo   !count!. !hookname!
            set "hooktype!count!=!hookname!"
        )
    )
)

echo.
set /p selection="Select hook types to install (e.g., 1,3,5) or 'all' for all hooks: "

if /i "%selection%"=="all" (
    REM Install all hooks
    for /d %%i in ("%SCRIPT_DIR%*") do (
        if exist "%%i\README.md" (
            call :copy_hook_type "%%i"
        )
    )
) else (
    REM Install selected hooks
    for %%s in (%selection%) do (
        set "selected=%%s"
        call :copy_selected_hook !selected!
    )
)
goto :eof

REM ==============================================================================
REM Function to copy a specific hook type
REM ==============================================================================
:copy_hook_type
set "source_dir=%~1"
set "hooktype=%~n1"

echo [INFO] Installing %hooktype% hooks...
REM Generate a Python aggregator to run all .hook scripts in this hooktype directory
(
    echo import sys, subprocess, os, glob
    echo hook_dir = r"%source_dir%"
    echo exit_code = 0
    echo for path in sorted(glob.glob(os.path.join(hook_dir, "*.hook"))):
    echo ^    print(f"[dispatcher] Running {path}...")
    echo ^    r = subprocess.run([sys.executable, path] + sys.argv[1:])
    echo ^    if r.returncode != 0:
    echo ^        sys.exit(r.returncode)
    echo sys.exit(0)
) > "%HOOKS_DIR%\%hooktype%.py"

REM Create a .bat shim so Git on Windows can execute the aggregator reliably
(
    echo @echo off
    echo "%VENV_DIR%\Scripts\python.exe" "%HOOKS_DIR%\%hooktype%.py" %%*
) > "%HOOKS_DIR%\%hooktype%.bat"

REM Also create the bare hook file (no extension) to call the .bat for compatibility
(
    echo @echo off
    echo call "%HOOKS_DIR%\%hooktype%.bat" %%*
) > "%HOOKS_DIR%\%hooktype%"

echo [SUCCESS] Installed aggregator for %hooktype%
goto :eof

REM ==============================================================================
REM Function to copy selected hook by number
REM ==============================================================================
:copy_selected_hook
set "sel=%~1"
set "hooktype=!hooktype%sel%!"
if not "%hooktype%"=="" (
    call :copy_hook_type "%SCRIPT_DIR%!hooktype!"
)
goto :eof