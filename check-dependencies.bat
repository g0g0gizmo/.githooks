@echo off
echo Checking Git Hooks Dependencies...
echo ===================================

REM Check Python
python --version >nul 2>&1
if !errorlevel! equ 0 (
    python --version
) else (
    echo [ERROR] Python not found
)

REM Check virtual environment
if exist "C:\Users\g0g0g\Projects\.githooks\venv" (
    echo [SUCCESS] Virtual environment exists
) else (
    echo [WARNING] Virtual environment not found
)

REM Check dotenvx
dotenvx --version >nul 2>&1
if !errorlevel! equ 0 (
    echo [SUCCESS] dotenvx is available
) else (
    echo [WARNING] dotenvx not found
)

REM Check Maven
mvn --version >nul 2>&1
if !errorlevel! equ 0 (
    echo [SUCCESS] Maven is available
) else (
    echo [WARNING] Maven not found
)

pause
