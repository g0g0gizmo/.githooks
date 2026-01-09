# Git Hooks - Advanced Git Hook Management

![Build Status](https://github.com/YOUR_ORG/githooks/workflows/CI/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)

**A comprehensive, cross-platform collection of Git hooks** to enforce code quality, commit conventions, and project workflows.

**Last Updated:** December 15, 2025

---

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Local Installation](#local-installation)
  - [Global Installation](#global-installation)
- [Available Hooks](#available-hooks)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- ✅ **13 Git Hook Types**: Comprehensive coverage (pre-commit, commit-msg, pre-push, etc.)
- ✅ **Cross-Platform**: Works on Windows, macOS, Linux
- ✅ **Python 3.9+**: Modern Python implementation
- ✅ **Conventional Commits**: Enforces semantic commit messages
- ✅ **Git Flow Integration**: Automated versioning and branch management
- ✅ **Dual Issue Tracking**: JIRA and GitHub Issues support (auto-detects from branch names)
- ✅ **JIRA Integration**: Automatic issue tracking and transitions
- ✅ **GitHub Issues**: Automatic labeling, comments, and state management
- ✅ **Code Formatting**: Auto-format with Black, isort, flake8
- ✅ **Branch Protection**: Prevent commits to main/develop
- ✅ **Spell Check**: Markdown linting with custom dictionaries
- ✅ **Modular Design**: Enable/disable individual hooks
- ✅ **Error Resilience**: Graceful handling of Win32 application errors

---

## Quick Start

Install hooks in 3 commands:

```bash
# Clone or download repository
git clone https://github.com/YOUR_ORG/githooks.git
cd githooks

# Run installer (choose your platform - runs in current directory)
python install.py              # All platforms (recommended)
./install.bat                  # Windows CMD
./install.ps1                  # PowerShell
./install.sh                   # Bash/Zsh (macOS/Linux)

# Verify installation
git commit --allow-empty -m "test: verify hooks installed"
```

Hooks are now active! Try making a commit to see them in action.

---

## Installation

### Prerequisites

- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **Git 2.0+** ([Download](https://git-scm.com/downloads))

**Verify prerequisites**:

```bash
python --version  # Should be 3.9 or higher
git --version     # Should be 2.0 or higher
```

### Local Installation

Install hooks for a **single repository**:

```bash
# Navigate to your repository
cd /path/to/your/repo

# Run installer (choose your platform)
python /path/to/githooks/install.py
# OR
/path/to/githooks/install.bat              # Windows CMD
/path/to/githooks/install.ps1              # PowerShell
/path/to/githooks/install.sh               # Bash/Zsh
```

Hooks are installed to `.git/hooks/` in your repository.

### Global Installation

Install hooks for **all repositories** on your system:

```bash
# Python (all platforms)
python install.py --global

# Platform-specific wrappers
install.bat . global              # Windows CMD
install.ps1 -Global               # PowerShell
install.sh --global               # Bash/Zsh
```

Git will use these hooks for all new repositories. Existing repositories require manual installation.

### Advanced Options

```bash
# Force reinstall (overwrite existing hooks)
python install.py --force

# Install to specific repository
python install.py --repo-path /path/to/repo

# Combine options
python install.py --global --force
```

---

## Available Hooks

| Hook Type              | Trigger                            | Purpose                                                    |
| ---------------------- | ---------------------------------- | ---------------------------------------------------------- |
| **pre-commit**         | Before commit is created           | Format code, check branch protection, spell check markdown |
| **prepare-commit-msg** | Before commit message editor opens | Auto-classify commit type from diff                        |
| **commit-msg**         | After commit message written       | Validate conventional commit format, JIRA issue numbers    |
| **post-commit**        | After commit created               | Auto-version bumping with conventional commits             |
| **pre-push**           | Before pushing to remote           | Protect main/develop branches, run tests                   |
| **post-checkout**      | After checking out branch          | JIRA ticket transition, cleanup pyc files                  |
| **pre-rebase**         | Before rebasing                    | Prevent rebase of protected branches                       |

---

## Configuration

Hooks use **git config** for configuration. No external files required.

### Essential Configuration

```bash
# Set your identity (required)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Hook Configuration

```bash
# Branch Protection
git config hooks.protectedBranches "main,develop,master"

# Commit Message Validation
git config hooks.requireIssueNumber true
git config hooks.issuePattern "PROJ-\d+"  # JIRA pattern

# Code Formatting
git config hooks.autoFormat true  # Auto-format on commit
git config hooks.formatters "black,isort,flake8"  # Comma-separated

# Git Flow
git config gitflow.branch.master "main"
git config gitflow.branch.develop "develop"
git config gitflow.prefix.feature "feature/"
git config gitflow.prefix.release "release/"
git config gitflow.prefix.hotfix "hotfix/"

# JIRA Integration (optional)
git config hooks.jira.url "https://your-org.atlassian.net"
git config hooks.jira.username "your.email@example.com"
# Password stored securely via keyring (prompted on first use)

# GitHub Issues Integration (optional)
export GITHUB_TOKEN="ghp_your_token_here"  # For automatic issue updates
```

### Issue Tracking Support

The hooks support both JIRA and GitHub Issues, automatically detecting which one to use based on your branch name:

**JIRA Branches:**
- `JT_PTEAE-2930_feature-description`
- `PROJ-123_fix-bug`
- Pattern: `[A-Z]+-\d+`

**GitHub Issue Branches:**
- `issue-123-description`
- `gh-123-fix-bug`
- `123-simple-fix`
- Pattern: `(?:issue|gh|#)?-?(\d+)`

See [GitHub Issues Integration Guide](docs/GITHUB-ISSUES-INTEGRATION.md) for detailed setup and usage.

**View all hook configuration**:

```bash
git config --get-regexp hooks\.
```

---

## Usage Examples

### Example 1: Conventional Commit Validation

```bash
# ❌ This will fail (invalid format)
git commit -m "updated some stuff"
# Error: Commit message must follow format: type(scope): description

# ✅ This will succeed
git commit -m "feat(auth): add JWT token refresh"
```

### Example 2: Branch Protection

```bash
# ❌ This will fail (committing to main)
git checkout main
git commit -m "fix: quick fix"
# Error: Direct commits to 'main' are not allowed. Create a feature branch.

# ✅ This will succeed
git checkout -b fix/auth-bug
git commit -m "fix(auth): handle null user object"
```

### Example 3: Auto-Formatting

```bash
# Make changes to Python file
echo "def foo( ):pass" >> myfile.py

# Commit triggers auto-formatting
git add myfile.py
git commit -m "feat(api): add foo function"
# Output:
# [pre-commit] Formatting with black... ✅ 1 file reformatted
# [pre-commit] Formatting with isort... ✅ 1 file reformatted
# [pre-commit] Linting with flake8... ✅ No issues found
```

### Example 4: Git Flow with Auto-Versioning

```bash
# Initialize git flow
python flow-init.py

# Start a feature
python flow-start.py feature my-awesome-feature

# Make commits with conventional format
git commit -m "feat(core): add new feature"
git commit -m "test(core): add feature tests"

# Finish feature (auto-calculates version bump)
git flow feature finish my-awesome-feature
# Output: Version bumped: 1.2.3 → 1.3.0 (minor)
```

---

## Troubleshooting

### Issue: Hooks not executing

**Symptoms**: Commits succeed without any hook output

**Solutions**:

1. Verify hooks installed: `ls -la .git/hooks/`
2. Check hook executable: `chmod +x .git/hooks/pre-commit`
3. Verify Python path in shebang: `head -1 .git/hooks/pre-commit`
4. Test hook manually: `.git/hooks/pre-commit`

### Issue: Python version error

**Symptoms**: `ImportError: Python 3.9+ required`

**Solutions**:

1. Check Python version: `python --version`
2. Install Python 3.9+: [python.org/downloads](https://www.python.org/downloads/)
3. Update shebang in hooks to correct Python path

### Issue: Dependencies not found

**Symptoms**: `ModuleNotFoundError: No module named 'keyring'`

**Solutions**:

1. Activate virtual environment: `source .venv/bin/activate` (Unix) or `.venv\Scripts\activate` (Windows)
2. Install dependencies: `pip install -r requirements.txt`
3. Reinstall hooks: `pwsh install-all.ps1 -Force`

### Issue: PowerShell execution policy error

**Symptoms**: `... cannot be loaded because running scripts is disabled...`

**Solutions**:

```powershell
# Temporarily allow scripts for current session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Run installer
pwsh install-all.ps1
```

### Issue: ModuleNotFoundError in hooks

**Symptoms**: `ModuleNotFoundError: No module named 'jira'` or similar import errors

**Cause**: Hook requires Python packages not installed in active environment.

**Solutions**:

```bash
# Option 1: Activate project venv and install dependencies
.\venv\Scripts\Activate.ps1      # Windows
source venv/bin/activate          # Unix
pip install -r requirements.txt

# Option 2: Install globally
pip install --user jira keyring typer

# Option 3: Verify which Python hooks are using
python -c "import sys; print(sys.executable)"
```

### Issue: Hooks use wrong Python version

**Symptoms**: Hook fails with "Python 3.9+ required" but you have 3.11 installed.

**Cause**: Multiple Python installations, hooks finding wrong one via PATH.

**Solutions**:

```bash
# Check which python3 is first in PATH
where python3      # Windows
which python3      # Unix

# Verify version
python3 --version

# Fix: Adjust PATH or use explicit shebang in hooks
# Edit hook file first line:
#!C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe
```

### Issue: Hooks work manually but fail in Git

**Symptoms**: Running `python pre-commit/format-code.hook` works, but `git commit` fails.

**Cause**: Different environment when Git executes hooks (minimal PATH, no venv).

**Solutions**:

```bash
# Ensure venv is activated BEFORE running Git commands
.\venv\Scripts\Activate.ps1
git commit -m "test"

# Alternative: Configure Git to use specific Python
git config core.pythonPath "C:\path\to\python.exe"

# Debug: Check Git's environment
git config --list | grep -i python
```

### Issue: Git config not found

**Symptoms**: `Error: hooks.protectedBranches not configured`

**Solutions**:

```bash
# Set required configuration
git config hooks.protectedBranches "main,develop"
```

---

## Architecture

### Dispatcher Pattern

Hooks use a **modular dispatcher pattern** for flexibility and maintainability:

```
.git/hooks/pre-commit          ← Dispatcher (auto-generated)
    ├── Executes all *.hook files in pre-commit/ directory
    └── Stops on first failure (non-zero exit code)

pre-commit/
    ├── format-code.hook        ← Individual hook (Black, isort)
    ├── spell-check-md-files.hook
    └── prevent-commit-to-main-or-develop.hook
```

**Key Features**:

- **Sequential Execution**: Hooks run in alphabetical order
- **Early Exit**: First hook failure stops execution
- **Subprocess Isolation**: Each hook runs as separate process (security)
- **Language Agnostic**: Any executable file with proper shebang works

**Example Dispatcher** (auto-generated by installer):

```python
#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

hooks_dir = Path(r'C:\path\to\githooks\pre-commit')
hook_files = sorted(hooks_dir.glob('*.hook'))

exit_code = 0
for hook_file in hook_files:
    if not hook_file.is_file():
        continue
    result = subprocess.run(
        [sys.executable, str(hook_file)],
        shell=False,
        check=False,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr, end='')
        exit_code = result.returncode
        break
sys.exit(exit_code)
```

### Python Environment

**Version 2.0.0+ (Current)**: Hooks use **system or project Python** directly.

- **No isolated venv**: Installer does not create `.githooks/venv/`
- **Respects active environment**: Hooks use whatever Python is in PATH
- **Project dependencies**: Install hook requirements in your project venv

**Migration from v1.x**: See [docs/MIGRATION.md](./docs/MIGRATION.md) for breaking changes.

**Recommended Setup**:

```bash
# Create project virtual environment
python -m venv venv

# Activate environment
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Unix

# Install hook dependencies
pip install -r requirements.txt

# Hooks will use this environment
git commit -m "test"
```

### Security Model

- **No `exec()` or `eval()`**: All hooks execute via `subprocess.run()` (shell=False)
- **Subprocess isolation**: Hooks cannot access installer process namespace
- **Shebang validation**: Only executable files with valid shebangs run
- **No shell injection**: Arguments passed as lists, never interpolated strings

---

## Contributing

We welcome contributions! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for:

- Development environment setup
- Running tests locally
- Code style guidelines
- Commit message conventions
- Pull request process

**Quick contribution setup**:

```bash
# Clone repository
git clone https://github.com/YOUR_ORG/githooks.git
cd githooks

# Install development dependencies
pip install -r requirements.txt

# Run tests (when available)
pytest tests/

# Run linting
black .
flake8 .
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## Credits

- Inspired by [pre-commit framework](https://pre-commit.com/)
- Git Flow implementation based on [nvie/gitflow](https://github.com/nvie/gitflow)
- Conventional Commits spec: [conventionalcommits.org](https://www.conventionalcommits.org/)

---

**Questions or Issues?** [Open an issue](https://github.com/YOUR_ORG/githooks/issues) or contact the maintainers.

# Hook validation test
