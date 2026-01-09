# Git Hooks Installation Guide

A step-by-step guide to installing and configuring Git hooks for different platforms and use cases.

**Last Updated:** January 6, 2026

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation Methods](#installation-methods)
  - [Local Installation (Single Repository)](#local-installation-single-repository)
  - [Global Installation (All Repositories)](#global-installation-all-repositories)
  - [Project-Specific Installation](#project-specific-installation)
- [Platform-Specific Setup](#platform-specific-setup)
  - [Windows (PowerShell/CMD)](#windows-powershellcmd)
  - [macOS](#macos)
  - [Linux](#linux)
- [Hook-Specific Dependencies](#hook-specific-dependencies)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Uninstallation](#uninstallation)

---

## Prerequisites

### System Requirements

| Component   | Minimum    | Recommended                 |
| ----------- | ---------- | --------------------------- |
| **Python**  | 3.9        | 3.10+                       |
| **Git**     | 2.0        | 2.30+                       |
| **Bash**    | 3.0        | 4.0+ (for Windows Git Bash) |
| **Node.js** | (optional) | 16.0+ (for commitlint)      |

### Verify Prerequisites

```bash
# Check Python version
python --version          # Should be 3.9 or higher
python -m pip --version   # Should show pip version

# Check Git version
git --version             # Should be 2.0 or higher

# Check Bash (if using Windows)
bash --version            # If using Git Bash
```

### Install Prerequisites

**Windows:**

```powershell
# Download Python from https://www.python.org/downloads/
# Download Git from https://git-scm.com/download/win
# Python installer includes pip
```

**macOS:**

```bash
# Using Homebrew
brew install python@3.11 git

# Or manually: https://www.python.org/downloads/
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt-get update
sudo apt-get install python3.11 python3.11-pip git
```

---

## Quick Start

The fastest way to get started:

```bash
# 1. Clone or navigate to the githooks repository
cd /path/to/your/repository

# 2. Run installer (works on all platforms)
python install.py

# 3. Verify installation
git commit --allow-empty -m "test: verify hooks"
```

Done! Hooks are now active and enforcing your standards.

---

## Installation Methods

### Local Installation (Single Repository)

Install hooks for a **single repository only** (recommended for most users).

```bash
# Navigate to your repository
cd /path/to/your/repository

# Run installer
python /path/to/githooks/install.py
# OR use wrapper script
./install.sh              # macOS/Linux
.\install.bat             # Windows CMD
.\install.ps1             # Windows PowerShell
```

**What happens:**

- Hooks are installed to `.git/hooks/` (local to repository)
- Hooks run only when you commit in this repository
- Only affects this repository, not others on your system

**Verify:**

```bash
ls .git/hooks/       # Should see dispatcher hooks
```

### Global Installation (All Repositories)

Install hooks for **all repositories** on your system.

```bash
# From any location
python /path/to/githooks/install.py --global
```

**What happens:**

- Hooks are installed to `~/.git-hooks/` (user home directory)
- Configure Git to use global hooks: `git config --global core.hooksPath ~/.git-hooks`
- Hooks run for every repository on your system
- Individual repositories can override with local hooks

**Verify:**

```bash
ls ~/.git-hooks/     # Should see dispatcher hooks
git config --global core.hooksPath  # Should show ~/.git-hooks
```

### Project-Specific Installation

Install for a **specific repository in a CI/CD pipeline** or deployment script.

```bash
# Specify target repository
python install.py --repo-path /path/to/repo

# Force reinstall (overwrite existing hooks)
python install.py --force

# Skip dependency checks
python install.py --skip-deps
```

---

## Platform-Specific Setup

### Windows (PowerShell/CMD)

#### PowerShell Installation

```powershell
# Navigate to githooks directory
cd C:\path\to\githooks

# Run PowerShell installer
.\install.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install.ps1
```

#### CMD Installation

```cmd
# Navigate to githooks directory
cd C:\path\to\githooks

# Run batch installer
install.bat
```

#### Python Installation (Recommended)

```powershell
# Navigate to your repository
cd C:\path\to\repo

# Run Python installer (works everywhere)
python C:\path\to\githooks\install.py
```

**Windows Path Considerations:**

- Python shebang: Use `#!/usr/bin/env python` (NOT `python3`)
- Git Bash path: Automatically detected and hard-coded during installation
- Path conversion: `C:\Users\...` → `C:/Users/...` for Bash compatibility

### macOS

```bash
# Install Python (if needed)
brew install python@3.11

# Navigate to your repository
cd /path/to/repo

# Run installer
python /path/to/githooks/install.py

# Or use bash wrapper
bash /path/to/githooks/install.sh
```

**macOS Path Considerations:**

- Python 3 is required (Python 2 is deprecated)
- `/usr/bin/env python3` may need explicit Python 3 reference
- Use `/usr/local/bin/python3` if env-based resolution fails

### Linux

```bash
# Install Python (if needed)
sudo apt-get install python3 python3-pip git

# Navigate to your repository
cd /path/to/repo

# Run installer
python3 /path/to/githooks/install.py

# Or use bash wrapper
bash /path/to/githooks/install.sh
```

**Linux Path Considerations:**

- Use `python3` explicitly on systems with both Python 2 and 3
- Ensure git and bash are in PATH
- Check file permissions: `chmod +x install.sh`

---

## Hook-Specific Dependencies

Some hooks require additional dependencies. Check before installing:

### Core Hooks (No Additional Dependencies)

These hooks work immediately after installation:

- `prevent-commit-to-main-or-develop.hook` - Branch protection
- `verify-name-and-email.hook` - Git config validation
- `search-term.hook` - Search for prohibited terms
- `prevent-bad-push.hook` - WIP prevention
- `prevent-rebase.hook` - Protected branch rebase prevention
- `new-branch-alert.hook` - Branch switch notifications
- `delete-pyc-files.hook` - Python cleanup

### Optional Hooks (Require Additional Tools)

#### Conventional Commit Validation

```bash
# Install Node.js (if not already installed)
# https://nodejs.org/

# Install commitlint globally
npm install -g @commitlint/cli @commitlint/config-conventional

# Hook uses this tool:
# commit-msg/conventional-commitlint.hook
```

#### Environment Variable Validation

```bash
# Install dotenvx globally
npm install -g @dotenvx/cli

# OR via pip
pip install python-dotenv

# Hook uses this tool:
# pre-commit/dotenvx.hook
```

#### Markdown Spell Checking

```bash
# Install Python spell checker
pip install pyspellchecker

# Hook uses this tool:
# pre-commit/spell-check-md-files.hook
```

#### JIRA Integration

```bash
# Install Python JIRA client
pip install jira>=3.6.0

# Install keyring for secure credential storage
pip install keyring>=24.3.0

# Hooks use these tools:
# post-checkout/jira-transition-worklog.hook
# pre-push/jira-add-push-worklog.hook
```

### Check Installed Dependencies

```bash
# Check Python packages
pip list | grep -E "jira|keyring|pyspellchecker"

# Check Node packages
npm list -g @commitlint/cli

# Check dotenvx
dotenvx --version
```

### Install from requirements.txt

```bash
# Install all Python dependencies
pip install -r requirements.txt

# Or use your project's virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## Verification

After installation, verify hooks are working correctly.

### 1. Check Installed Hooks

```bash
# Local installation
ls -la .git/hooks/

# Global installation
ls -la ~/.git-hooks/
```

You should see dispatcher hooks for each hook type:

```text
pre-commit
prepare-commit-msg
commit-msg
pre-push
post-checkout
pre-rebase
```

### 2. Test Dispatcher Execution

```bash
# Test pre-commit dispatcher
bash .git/hooks/pre-commit

# Should output:
# [dispatcher] Running verify-name-and-email.hook...
# [dispatcher] verify-name-and-email.hook exited with code 0
# [dispatcher] Running search-term.hook...
# ...
```

### 3. Test Commit

```bash
# Create a test commit
git commit --allow-empty -m "test: verify hooks installed"

# You should see hook output before commit completes
```

### 4. Verify Git Config

```bash
# For local installation, nothing needed
# For global installation, verify config:
git config --global core.hooksPath
# Should show: ~/.git-hooks

# For local installation in specific repo:
git config --local core.hooksPath
# Should show: .git/hooks
```

---

## Troubleshooting

### Issue: "Hook not found" or "Permission denied"

**Cause:** Hooks are not executable or not found

**Solution:**

```bash
# Make hooks executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/commit-msg

# Or fix all hooks at once:
chmod +x .git/hooks/*
```

### Issue: "Python not found" or "python3: command not found"

**Cause:** Python is not in PATH or wrong version

**Solution:**

```bash
# Verify Python is installed
python --version   # or python3 --version

# Reinstall hooks with explicit Python path
/usr/local/bin/python3 install.py

# Or edit dispatcher to use explicit Python path
# (will be done automatically if needed)
```

### Issue: "ModuleNotFoundError" for jira, keyring, etc

**Cause:** Optional dependencies not installed

**Solution:**

```bash
# Install missing module
pip install jira keyring

# Or disable the hook temporarily
mv .git/hooks/post-checkout/jira-transition-worklog.hook \
   .git/hooks/post-checkout/jira-transition-worklog.hook.disabled
```

### Issue: Hooks run but don't do anything

**Cause:** Hooks are not being triggered correctly

**Solution:**

```bash
# Verify Git recognizes hooks directory
git config core.hooksPath

# Force reinstall
python install.py --force

# Check hook output verbosity
bash .git/hooks/pre-commit
```

### Issue: "Permission denied: install.py" on macOS/Linux

**Cause:** Install script not executable

**Solution:**

```bash
# Make install script executable
chmod +x install.sh
./install.sh

# Or use Python directly
python install.py
```

### Issue: Windows Git Bash path errors

**Cause:** Incompatible path format for Bash

**Solution:**

The installer automatically detects and converts paths:

```powershell
# Verify Git Bash is installed
where git        # Should find git.exe

# If not found, install Git from https://git-scm.com/download/win
```

### Issue: Hooks slow down commits significantly

**Cause:** Too many hooks or slow external tools

**Solution:**

```bash
# Temporarily disable a hook
mv .git/hooks/hook-name.hook .git/hooks/hook-name.hook.disabled

# Verify which hook is slow
bash .git/hooks/pre-commit
# Look for timing in output

# Check for network calls to JIRA, GitHub, etc.
# Consider async execution for slow operations
```

### Enable Debug Output

```bash
# Run hooks with debug output
bash -x .git/hooks/pre-commit

# Or set environment variable
DEBUG=1 git commit -m "test"
```

---

## Uninstallation

### Remove Hooks

**Local Repository:**

```bash
# Remove local hooks
rm -rf .git/hooks

# Reinitialize hooks (resets to Git defaults)
git init
```

**Global Installation:**

```bash
# Remove global hooks directory
rm -rf ~/.git-hooks

# Unset global hooks path
git config --global --unset core.hooksPath
```

### Disable Specific Hooks

```bash
# Instead of uninstalling, just disable a hook
mv .git/hooks/pre-commit/my-hook.hook \
   .git/hooks/pre-commit/my-hook.hook.disabled

# Dispatcher will skip .disabled files
```

### Restore Git Defaults

```bash
# This will use Git's default (empty) hooks
rm -rf .git/hooks
git init
```

---

## Getting Help

- **Installation Issues:** Check [Troubleshooting](#troubleshooting) section
- **Hook Documentation:** See `.github/copilot-instructions.md`
- **Configuration:** See each hook's README in the hook directory
- **Report Issues:** Submit bug reports with:
  - Python version (`python --version`)
  - Git version (`git --version`)
  - Operating system
  - Steps to reproduce
