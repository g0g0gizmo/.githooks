@echo off
setlocal enabledelayedexpansion

REM Simple batch script to install a Git hook
REM Usage: install-hook.bat <repo-path> <hook-type> [specific-hook-file]
REM Example: install-hook.bat "C:\my\repo" "pre-commit" "format-code.hook"

if "%~1"=="" (
    echo Usage: install-hook.bat ^<repo-path^> ^<hook-type^> [specific-hook-file]
    echo Example: install-hook.bat "C:\my\repo" "pre-commit" "format-code.hook"
    echo.
    echo Available hook types:
    for /d %%i in (*) do (
        if exist "%%i\README.md" echo   %%i
    )
    exit /b 1
)

set "REPO_PATH=%~1"
set "HOOK_TYPE=%~2"
set "SPECIFIC_HOOK=%~3"

REM Check if repository exists and has .git directory
if not exist "%REPO_PATH%\.git" (
    echo Error: %REPO_PATH% is not a Git repository
    exit /b 1
)

REM Check if hook type directory exists
if not exist "%HOOK_TYPE%" (
    echo Error: Hook type '%HOOK_TYPE%' not found
    echo Available hook types:
    for /d %%i in (*) do (
        if exist "%%i\README.md" echo   %%i
    )
    exit /b 1
)

set "HOOKS_DIR=%REPO_PATH%\.git\hooks"
set "SOURCE_DIR=%~dp0%HOOK_TYPE%"

REM Create hooks directory if it doesn't exist
if not exist "%HOOKS_DIR%" mkdir "%HOOKS_DIR%"

REM If specific hook file is provided, use it
if not "%SPECIFIC_HOOK%"=="" (
    if exist "%SOURCE_DIR%\%SPECIFIC_HOOK%" (
        copy "%SOURCE_DIR%\%SPECIFIC_HOOK%" "%HOOKS_DIR%\%HOOK_TYPE%"
        if !errorlevel! equ 0 (
            echo Successfully installed %HOOK_TYPE% hook from %SPECIFIC_HOOK%
        ) else (
            echo Failed to install %HOOK_TYPE% hook
            exit /b 1
        )
    ) else (
        echo Error: Hook file '%SPECIFIC_HOOK%' not found in %HOOK_TYPE% directory
        exit /b 1
    )
) else (
    REM List available hooks and let user choose
    echo Available %HOOK_TYPE% hooks:
    set /a count=0
    for %%f in ("%SOURCE_DIR%\*") do (
        if not "%%~nxf"=="README.md" (
            set /a count+=1
            echo   !count!. %%~nxf
            set "hook!count!=%%~nxf"
        )
    )
    
    if !count! equ 0 (
        echo No hooks found in %HOOK_TYPE% directory
        exit /b 1
    )
    
    if !count! equ 1 (
        REM Only one hook, install it automatically
        copy "%SOURCE_DIR%\!hook1!" "%HOOKS_DIR%\%HOOK_TYPE%"
        if !errorlevel! equ 0 (
            echo Successfully installed %HOOK_TYPE% hook from !hook1!
        ) else (
            echo Failed to install %HOOK_TYPE% hook
            exit /b 1
        )
    ) else (
        REM Multiple hooks, ask user to choose
        set /p choice="Select hook to install (1-!count!): "
        
        if defined hook!choice! (
            copy "%SOURCE_DIR%\!hook%choice%!" "%HOOKS_DIR%\%HOOK_TYPE%"
            if !errorlevel! equ 0 (
                echo Successfully installed %HOOK_TYPE% hook from !hook%choice%!
            ) else (
                echo Failed to install %HOOK_TYPE% hook
                exit /b 1
            )
        ) else (
            echo Invalid selection
            exit /b 1
        )
    )
)

echo.
echo Hook installed in: %HOOKS_DIR%\%HOOK_TYPE%
echo The hook will now run automatically for %HOOK_TYPE% events in this repository.