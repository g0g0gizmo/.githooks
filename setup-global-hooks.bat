@echo off
setlocal enabledelayedexpansion

REM Script to set up global Git hooks
REM Usage: setup-global-hooks.bat [hooks-directory]

set "DEFAULT_HOOKS_DIR=%USERPROFILE%\.git-hooks"
set "HOOKS_DIR=%~1"

if "%HOOKS_DIR%"=="" (
    set "HOOKS_DIR=%DEFAULT_HOOKS_DIR%"
)

echo Setting up global Git hooks...
echo Global hooks directory: %HOOKS_DIR%

REM Create the global hooks directory if it doesn't exist
if not exist "%HOOKS_DIR%" (
    mkdir "%HOOKS_DIR%"
    echo Created global hooks directory: %HOOKS_DIR%
)

REM Configure Git to use the global hooks directory
git config --global core.hooksPath "%HOOKS_DIR%"
if !errorlevel! equ 0 (
    echo Configured Git to use global hooks directory
) else (
    echo Failed to configure Git global hooks path
    exit /b 1
)

REM Copy hooks to global directory
echo.
echo Available hook types:
set /a count=0
for /d %%i in (*) do (
    if exist "%%i\README.md" (
        set /a count+=1
        echo   !count!. %%i
        set "hooktype!count!=%%i"
    )
)

echo.
set /p selection="Select hook types to install globally (e.g., 1,3,5) or 'all' for all hooks: "

if /i "%selection%"=="all" (
    REM Install all hooks
    for /d %%i in (*) do (
        if exist "%%i\README.md" (
            call :InstallHookType "%%i"
        )
    )
) else (
    REM Install selected hooks
    for %%s in (%selection%) do (
        if defined hooktype%%s (
            call :InstallHookType "!hooktype%%s!"
        )
    )
)

echo.
echo Global Git hooks setup completed!
echo All new and existing Git repositories will now use these hooks.
echo.
echo Global hooks directory: %HOOKS_DIR%
echo To disable global hooks: git config --global --unset core.hooksPath
echo To check current setting: git config --global core.hooksPath
goto :eof

:InstallHookType
set "HOOK_TYPE=%~1"
set "SOURCE_DIR=%~dp0%HOOK_TYPE%"

REM Count available hooks of this type
set /a hook_count=0
for %%f in ("%SOURCE_DIR%\*") do (
    if not "%%~nxf"=="README.md" (
        set /a hook_count+=1
        set "hook_file!hook_count!=%%~nxf"
    )
)

if !hook_count! equ 0 (
    echo No hooks found in %HOOK_TYPE% directory
    goto :eof
)

if !hook_count! equ 1 (
    REM Only one hook, install it automatically
    copy "%SOURCE_DIR%\!hook_file1!" "%HOOKS_DIR%\%HOOK_TYPE%" >nul
    if !errorlevel! equ 0 (
        echo Installed global hook: %HOOK_TYPE% ^(!hook_file1!^)
    ) else (
        echo Failed to install %HOOK_TYPE% hook
    )
) else (
    REM Multiple hooks, use the first one or let user choose later
    copy "%SOURCE_DIR%\!hook_file1!" "%HOOKS_DIR%\%HOOK_TYPE%" >nul
    if !errorlevel! equ 0 (
        echo Installed global hook: %HOOK_TYPE% ^(!hook_file1!^)
    ) else (
        echo Failed to install %HOOK_TYPE% hook
    )
)
goto :eof