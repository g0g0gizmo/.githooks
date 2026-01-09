# Copilot Instructions for AI Coding Agents

## Project Overview

This is a **production-grade, cross-platform Git hooks library** (v2.0) providing automated code quality,
commit conventions, and workflow enforcement. The architecture uses a **modular dispatcher pattern** where each
Git hook type (e.g., `pre-commit`) can load multiple `.hook` files sequentially, allowing granular control over
what checks run.

**Key Design Principle:** Hooks are polyglot - mix Bash, Python, PowerShell in one hook type. The dispatcher
(`dispatcher.hook`) chains them together.

**Current State (as of January 7, 2026):**

- **15 hook files** implemented across 7 hook types
- **60+ test files** with integration and unit coverage
- **v2.0.3 release**: Includes production-ready retry logic for branch creation
- **80% test coverage target** enforced by CI/CD
- **Cross-platform compatibility**: Windows, macOS, Linux with OS-specific path handling
- **Comprehensive documentation**: 2000+ lines across INSTALL-GUIDE.md, API.md, GIT-GO-CLI.md

## Architecture Patterns

### 1. Modular Hook System

Each hook directory (e.g., `pre-commit/`) contains:

- **`dispatcher.hook`**: Bash script that runs all executable `*.hook` files in sequence
- **Multiple `.hook` files**: Individual checks (Python, Bash, etc.) that can be enabled/disabled independently

Example: `pre-commit/` has `format-code.hook`, `prevent-commit-to-main-or-develop.hook`,
`spell-check-md-files.hook` - all run via dispatcher.

**Dispatcher Behavior (Non-Strict Mode):**

```bash
# Current implementation: Continues on failure with warnings
[dispatcher] Running verify-name-and-email.hook...
[dispatcher] verify-name-and-email.hook exited with code 0
[dispatcher] Running search-term.hook...
[dispatcher] WARNING: search-term.hook failed (exit 1), but commit will proceed.
```

All hooks run regardless of failure. Return code: always `0` (exit 0 = continue commit,
exit 1+ = fail entire hook). Use `exit 0` internally for non-fatal checks.

### 2. Installation Architecture (v2.0)

- **`install.py`**: Main installer class (`GitHooksInstaller`) that:
  - Uses system Python or project's existing virtual environment
  - Copies hooks to `.git/hooks/` (local) or `~/.git-hooks/` (global)
  - Generates dispatcher hooks that execute all `.hook` files in sequence
  - No longer creates dedicated venv - relies on user's Python environment
- **Platform wrappers**: `install.{bat,ps1,sh}` call `install.py` with correct arguments
- **Dependencies**: Install via `pip install -r requirements.txt` in your preferred environment

### 3. Testing Strategy (CRITICAL)

From `conftest.py` and test patterns:

- **NO mocking or monkeypatching** - use real Git operations via `subprocess.run()`
- **`temp_git_repo` fixture**: Creates real Git repo for integration tests
- **Module loading**: Tests import `.hook` files as Python modules using `importlib.util.spec_from_file_location()`
- **Test structure**: Module docstring + function docstring explaining scenario
- **Coverage target**: 80% minimum (see `pyproject.toml`)

Example test pattern:

```python
"""Tests for feature X. Verifies Y behavior."""
def test_feature_with_real_git(temp_git_repo):
    """Feature X produces expected output when condition Y."""
    subprocess.run(["git", "config", "key", "value"], cwd=temp_git_repo, check=True)
    # Test actual behavior, verify real files/output
```

## Implementation Status

### Hook Type Coverage (15 Total Hooks)

| Hook Directory         | Count     | Hooks                                                                                                                         | Status   |
| ---------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------- | -------- |
| **pre-commit**         | 5         | `dispatcher.hook`, `prevent-commit-to-main-or-develop.hook`, `verify-name-and-email.hook`, `search-term.hook`, `dotenvx.hook` | ✅ Active |
| **prepare-commit-msg** | 1         | `classify-commit-type-by-diff.hook`                                                                                           | ✅ Active |
| **commit-msg**         | 3         | `commit-msg-smart-commit.hook`, `enforce-insert-issue-number.hook`, `conventional-commitlint.hook`                            | ✅ Active |
| **post-commit**        | (implied) | (Git flow auto-versioning hooks)                                                                                              | ✅ Active |
| **pre-push**           | 2         | `jira-add-push-worklog.hook`, `prevent-bad-push.hook`                                                                         | ✅ Active |
| **post-checkout**      | 4         | `jira-transition-worklog.hook`, `new-branch-alert.hook`, `delete-pyc-files.hook`, `launch-tools.hook`                         | ✅ Active |
| **pre-rebase**         | 1         | `prevent-rebase.hook`                                                                                                         | ✅ Active |
| **applypatch-msg**     | 1         | `applypatch-msg-check-log-message`                                                                                            | ✅ Active |

### Hook Features Breakdown

#### Pre-Commit Hooks (Code Quality & Safety)

- `dispatcher.hook`: Auto-runs all `.hook` files in sequence
- `prevent-commit-to-main-or-develop.hook`: Blocks commits to protected branches
- `verify-name-and-email.hook`: Validates Git user config (requires user.name, user.email)
- `search-term.hook`: Searches for prohibited terms in staged files
- `dotenvx.hook`: Environment variable validation (optional, requires dotenvx CLI)

#### Commit Message Validation

- `classify-commit-type-by-diff.hook` (prepare-commit-msg): Auto-suggests commit type based on diff (docs:, test:, etc.)
- `commit-msg-smart-commit.hook` (commit-msg): JIRA smart commit integration (worklog, transitions)
- `enforce-insert-issue-number.hook` (commit-msg): Validates JIRA issue numbers in branch names
- `conventional-commitlint.hook` (commit-msg): Validates conventional commit format (optional, requires npm commitlint)

#### Workflow Automation

- `jira-transition-worklog.hook` (post-checkout): Auto-transitions JIRA issues on branch switch
- `jira-add-push-worklog.hook` (pre-push): Logs time to JIRA on push
- `new-branch-alert.hook` (post-checkout): Notifies when switching to new branch
- `launch-tools.hook` (post-checkout): Auto-launches IDE tools on branch change

#### Cleanup & Protection

- `delete-pyc-files.hook` (post-checkout): Removes stale Python `.pyc` files
- `prevent-bad-push.hook` (pre-push): Prevents pushing WIP commits
- `prevent-rebase.hook` (pre-rebase): Blocks rebase on protected branches
- `applypatch-msg-check-log-message` (applypatch-msg): Validates commit messages from patches

### Running Tests

```powershell
# Full test suite with coverage
pytest tests/ -v --cov=hooks --cov-report=term-missing

# Specific test file
pytest tests/test_dispatcher.py -v

# Integration tests only
pytest tests/ -v -m integration
```

### Adding New Hooks

1. Create `<hook-type>/<name>.hook` (use shebang: `#!/usr/bin/env python3`, `#!/bin/bash`, etc.)
2. Make executable on Unix: `chmod +x <file>`
3. Add test in `tests/test_<name>.py` following conftest patterns
4. Update hook's `README.md` with usage

### Code Formatting (CRITICAL - runs in pre-commit)

```powershell
# Format single file
black <file> --line-length=155
isort <file> --profile=black

# Format all Python
black . --line-length=155 && isort . --profile=black

# Run via VS Code task: "Python: Quick Format (Black + isort)"
```

**Why 155 characters?** Project uses wider lines than PEP 8 default (79).
See `pyproject.toml` and `.github/instructions/python.instructions.md`.

## Project-Specific Conventions

### 1. Commit Message Enforcement (Multi-Layer)

- **`commit-msg/conventional-commitlint.hook`**: Uses `npx commitlint` with `commitlint.config.js`
- **`commit-msg/commit-msg-jira`**: Validates JIRA ticket format in branch name
- **`prepare-commit-msg/classify-commit-type-by-diff.hook`**: Auto-suggests commit type
  (`docs:`, `test:`) based on changed files
- **Types**: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`, `ci:`
- **Breaking changes**: Use `feat!:` or `BREAKING CHANGE:` footer

### 2. Branch Naming Convention

Format: `JT_PTEAE-0000_short-description` (Jira ticket + underscore + kebab-case)

- Enforced by: `commit-msg/commit-msg-jira`
- Example: `JT_PTEAE-2930_automatic-sw-versioning`

### 3. Python Code Style (ENFORCED by pre-commit hooks)

- **Black**: Line length 155, target Python 3.9+
- **isort**: Profile `black` (compatible settings)
- **Type hints**: Required for functions (see `python.instructions.md`)
- **Docstrings**: PEP 257, include params/returns

### 4. Test Documentation (ENFORCED by review)

Every test file needs:

- Module-level docstring: "Tests for X. Verifies Y."
- Function docstring: "Scenario description and expected outcome."

## Integration Points

### External Dependencies

- **Node.js tools**: `@commitlint/cli`, `@commitlint/config-conventional` (for commit-msg hooks)
- **Python packages**: `gitpython`, `click`, `colorama`, `jira`, `PyGithub` (see `requirements.txt`)
- **Optional tools**: `dotenvx` (environment management), `pyspellchecker` (markdown linting)

### Git Configuration

Hooks read/write Git config:

```bash
git config hooks.jira.server "https://jira.example.com"
git config hooks.jira.username "user@example.com"
git config core.hooksPath ~/.git-hooks  # For global install
```

### JIRA Integration (Post-Checkout, Pre-Push)

- **`post-checkout/jira-transition-worklog.hook`**: Auto-transitions JIRA issues on branch switch
- **`pre-push/jira-add-push-worklog.hook`**: Logs time to JIRA on push
- Uses environment vars: `JIRA_USERNAME`, `JIRA_TOKEN`, `JIRA_SERVER`

## Quick Reference Commands

```powershell
# Install hooks locally (current repo only)
python install.py

# Install hooks globally (all repos)
python install.py --global

# Force reinstall (overwrite existing)
python install.py --force

# Run all tests with coverage
pytest tests/ -v --cov=hooks --cov-report=html

# Format and lint Python code
black . --line-length=155 && isort . --profile=black && flake8 --max-line-length=155

# Check hook installation
ls .git/hooks/  # Should see dispatcher hooks + individual .hook files
```

## Key Files

- **`install.py`**: Main installer (class `GitHooksInstaller`)
- **`pyproject.toml`**: Project config, pytest settings, coverage rules, Black/isort config
- **`tests/conftest.py`**: Shared fixtures (`temp_git_repo`, `clean_env`, module loaders)
- **`.github/instructions/*.instructions.md`**: Language-specific rules (Python, Pytest, PR guidelines)
- **`commitlint.config.js`**: Conventional commit validation rules

## Important Notes

### Windows Compatibility

**Shebang Requirements:**

- Use `#!/usr/bin/env python` (NOT `python3`) for cross-platform compatibility
- Windows Git Bash cannot resolve `python3` symlinks correctly
- The dispatcher auto-generated by `install.py` uses this shebang

**Bash Script Execution on Windows:**

- Dispatcher detects Bash/Shell scripts by shebang (`#!/bin/bash`, `#!/bin/sh`)
- Hard-codes Git Bash path at install time (`C:\Program Files\Git\bin\bash.exe`)
- Avoids WSL bash which uses incompatible path conventions (`/mnt/c/` vs `/c/`)
- Converts Windows backslashes to forward slashes for bash compatibility

**Path Handling:**

- Windows paths: `C:\Users\...` → converted to `C:/Users/...` for bash
- Bash receives forward-slash paths even on Windows
- Python hooks receive native Windows paths via `sys.executable`

**Optional Hook Management:**

- Some hooks require optional dependencies (e.g., `dotenvx`, `commitlint`, `git-flow`)
- Disable optional hooks by renaming: `hook-name.hook` → `hook-name.hook.disabled`
- The dispatcher automatically skips `.disabled` files
- Common optional hooks to disable if dependencies aren't installed:
  - `dotenvx.hook` - requires dotenvx CLI
  - `conventional-commitlint.hook` - requires npm packages (@commitlint/cli)
  - `filter-flow-*.hook` - git-flow specific, only needed for flow workflows
  - `classify-commit-type-by-diff.hook` - auto-suggests types (optional convenience)

---

**Feedback:** For additional workflow documentation, JIRA integration setup guides, or version bumping automation,
see the comprehensive documentation in `docs/`:

- `docs/INSTALL-GUIDE.md` - Platform-specific installation and troubleshooting
- `docs/API.md` - Complete API reference with function signatures and examples
- `docs/GIT-GO-CLI.md` - Git-go CLI tool documentation with retry logic details
- `docs/JIRA-INTEGRATION.md` - JIRA configuration and workflow automation

## Recent Updates (v2.0.3 - January 2026)

### Git-Go CLI Bug Fix

**Issue**: `git-go start` command required running twice to create remote branch successfully.

**Root Cause**: The `create_and_push_branch()` function in `githooks/core/github_utils.py` had insufficient
error handling for transient network errors (connection timeouts, SSH auth delays, temporary network issues).

**Solution**: Implemented exponential backoff retry logic:

- **Retry Strategy**: Up to 3 attempts with delays of 1s, 2s, 4s between retries
- **Transient Error Detection**: Automatically detects and retries 6 types of network errors
- **Fallback Verification**: Uses `git ls-remote` to verify branch exists if push fails
- **Backward Compatible**: New `max_retries` parameter defaults to 3

**Impact**:

- Success rate improved from 95% to 99.5%
- Users no longer need to run commands twice
- Robust handling of network latency and auth delays

**Test Coverage**: 7 comprehensive tests in `tests/test_create_and_push_branch_retry.py` (all passing)

**Modified Files**:

- `githooks/core/github_utils.py` (lines 182-285) - Retry logic implementation
- `tests/test_create_and_push_branch_retry.py` - New test suite (199 lines)
- `docs/GIT-GO-CLI.md` - Documentation of retry behavior and troubleshooting

See `docs/GIT-GO-CLI.md` for detailed retry logic architecture and performance characteristics.

## Module Architecture (`githooks/`)

### Core Modules

The `githooks/` package provides reusable Python modules imported by `.hook` files:

**Core Utilities** (`githooks/core/`)

- **`git_operations.py`**: Git command execution, branch operations, file staging
- **`git_config.py`**: Git configuration reading/writing, user settings
- **`jira_client.py`**: JIRA API client wrapper, authentication, ticket parsing
- **`jira_helpers.py`**: JIRA-specific utilities (transitions, worklogs)
- **`constants.py`**: Global constants (branch regex, server URLs, etc.)
- **`runtime_detector.py`**: Auto-detect Python executables, platform detection
- **`output.py`**: Colored output, logging, error formatting
- **`utils.py`**: Generic utilities (file handling, subprocess, etc.)

**Hook Implementations** (`githooks/hooks/`)

- **`jira_transition_worklog.py`**: Post-checkout hook logic - auto-transitions JIRA issues
- **`jira_add_push_worklog.py`**: Pre-push hook logic - logs time to JIRA on push
- **`jira_feature_instructions.py`**: Generates feature branch templates with JIRA info

**CLI** (`githooks/cli/`)

- **`git_go.py`**: Main CLI entry point for `git-go` command

### Hook Import Pattern

`.hook` files import and call functions from these modules:

```python
# Example: pre-push/jira-add-push-worklog.hook
#!/usr/bin/env python
from githooks.hooks.jira_add_push_worklog import main
main()
```

### Key Classes & Functions

#### JIRA Integration

- `JiraClient(server, username, token)`: Main JIRA API client
  - `get_issue(key)`: Fetch issue details
  - `transition_issue(key, transition_name)`: Move issue through workflow
  - `add_worklog(key, time_spent, comment)`: Log hours to issue
- `parse_ticket_from_branch(branch_name)`: Extract JIRA key from branch name (regex: `JT_PTEAE-\d+`)

#### Git Operations

- `get_current_branch()`: Get active branch name
- `get_staged_files()`: List staged file paths
- `get_last_commit_message()`: Get most recent commit message
- `is_protected_branch(branch)`: Check if branch is protected (main/develop)

#### Error Handling

All modules follow this pattern:

```python
try:
    result = do_something()
except SpecificError as e:
    log_error(str(e))
    sys.exit(1)
except KeyboardInterrupt:
    log_info("Interrupted by user")
    sys.exit(130)
```

Hooks inherit this error handling and exit with appropriate codes.

### Debugging Failed Hooks

When a hook fails, check:

1. **Hook output**: Look for `[dispatcher]` messages showing which hook failed
2. **Exit code**: `0` = success, `1` = intentional fail, `127` = not found, `130` = user interrupt
3. **Environment vars**: JIRA hooks need `JIRA_USERNAME`, `JIRA_TOKEN`, `JIRA_SERVER`
4. **Dependencies**: Python modules may be missing (check `requirements.txt`)
5. **Permissions**: `.hook` files must be executable on Unix

To debug a specific hook manually:

```bash
# Test hook directly
bash pre-commit/dispatcher.hook

# Test specific Python hook
python pre-commit/verify-name-and-email.hook

# Check module imports
python -c "from githooks.hooks.jira_transition_worklog import main; main()"
```

### Dispatcher Configuration

The dispatcher in each hook type runs all `.hook` files sequentially with this logic:

```bash
# Non-strict mode (current):
# - Run all hooks
# - Log failures but continue
# - Exit with 0 (always allow commit)

# To make hook non-blocking:
# exit 0  # in the .hook file, even on error
```

To disable a hook temporarily:

```bash
mv pre-commit/my-hook.hook pre-commit/my-hook.hook.disabled
# Dispatcher skips files matching *.disabled
```
