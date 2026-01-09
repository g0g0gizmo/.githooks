@echo off
REM ==============================================================================
REM Git Hooks Installer - Windows Batch Wrapper
REM ==============================================================================
REM This script is a simple wrapper that calls the Python install.py script
REM
REM Usage: install.bat [repo-path] [global|force|skip-deps]
REM
REM Examples:
REM   install.bat                          - Install in current directory
REM   install.bat "C:\my\project"          - Install in specific repository
REM   install.bat . global                 - Install globally
REM   install.bat . force                  - Force reinstall
REM ==============================================================================

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "INSTALL_PY=%SCRIPT_DIR%install.py"

REM Check if Python is available
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

REM Check if install.py exists
if not exist "%INSTALL_PY%" (
    echo [ERROR] install.py not found at %INSTALL_PY%
    pause
    exit /b 1
)

REM Build arguments for Python script
set "ARGS="
set "REPO_PATH=%~1"
set "FLAG1=%~2"
set "FLAG2=%~3"

REM Handle repo path
if not "%REPO_PATH%"=="" (
    if not "%REPO_PATH%"=="global" (
        if not "%REPO_PATH%"=="force" (
            if not "%REPO_PATH%"=="skip-deps" (
                set "ARGS=--repo-path "%REPO_PATH%""
            )
        )
    )
)

REM Handle flags
if /i "%REPO_PATH%"=="global" set "ARGS=!ARGS! --global"
if /i "%FLAG1%"=="global" set "ARGS=!ARGS! --global"
if /i "%FLAG2%"=="global" set "ARGS=!ARGS! --global"

if /i "%REPO_PATH%"=="force" set "ARGS=!ARGS! --force"
if /i "%FLAG1%"=="force" set "ARGS=!ARGS! --force"
if /i "%FLAG2%"=="force" set "ARGS=!ARGS! --force"

if /i "%REPO_PATH%"=="skip-deps" set "ARGS=!ARGS! --skip-deps"
if /i "%FLAG1%"=="skip-deps" set "ARGS=!ARGS! --skip-deps"
if /i "%FLAG2%"=="skip-deps" set "ARGS=!ARGS! --skip-deps"

REM Run the Python installer
echo Running: python "%INSTALL_PY%" %ARGS%
python "%INSTALL_PY%" %ARGS%

set EXIT_CODE=!errorlevel!
if !EXIT_CODE! neq 0 (
    echo.
    echo [ERROR] Installation failed with exit code !EXIT_CODE!
    pause
    exit /b !EXIT_CODE!
)

pause
exit /b 0
