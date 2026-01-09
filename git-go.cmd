@echo off
REM Windows wrapper for git-go custom command
REM Allows 'git go' to work on Windows by forwarding to Python script

python "%~dp0git-go" %*
