# Git Hooks Module API Reference

Complete API documentation for the `githooks/` Python module used by `.hook` files and CLI tools.

**Last Updated:** January 6, 2026

---

## Table of Contents

- [Module Overview](#module-overview)
- [Core Modules](#core-modules)
  - [git_operations](#git_operations)
  - [git_config](#git_config)
  - [jira_client](#jira_client)
  - [jira_helpers](#jira_helpers)
  - [output](#output)
  - [runtime_detector](#runtime_detector)
  - [constants](#constants)
  - [utils](#utils)
- [Hook Implementations](#hook-implementations)
- [Error Codes](#error-codes)
- [Performance Considerations](#performance-considerations)

---

## Module Overview

The `githooks/` package provides reusable modules for implementing Git hooks across different hook types.

```python
from githooks.core.git_operations import get_current_branch
from githooks.core.jira_client import JiraClient
from githooks.hooks.jira_transition_worklog import main as transition_worklog
```text

### Module Structure

```text
githooks/
├── core/                         # Core utilities
│   ├── git_operations.py        # Git command execution
│   ├── git_config.py            # Git configuration
│   ├── jira_client.py           # JIRA API client
│   ├── jira_helpers.py          # JIRA helpers
│   ├── constants.py             # Constants
│   ├── runtime_detector.py      # Runtime detection
│   ├── output.py                # Colored output
│   └── utils.py                 # Utilities
├── hooks/                        # Hook implementations
│   ├── jira_transition_worklog.py
│   ├── jira_add_push_worklog.py
│   └── jira_feature_instructions.py
├── cli/                          # CLI tools
│   └── git_go.py
└── __init__.py
```

---

## Core Modules

### git_operations

Git command execution and branch operations.

**Location:** `githooks/core/git_operations.py`

#### Functions

##### `get_current_branch() -> str`

Get the name of the currently checked-out branch.

**Returns:**

- `str`: Branch name (e.g., `main`, `feature/PTEAE-123`)

**Raises:**

- `RuntimeError`: If not in a Git repository

**Example:**

```python
from githooks.core.git_operations import get_current_branch

branch = get_current_branch()
print(f"Current branch: {branch}")
```

##### `get_staged_files() -> List[str]`

Get list of staged files ready to be committed.

**Returns:**

- `List[str]`: File paths of staged files

**Example:**

```python
from githooks.core.git_operations import get_staged_files

files = get_staged_files()
for file_path in files:
    print(f"Staged: {file_path}")
```

##### `get_last_commit_message() -> str`

Get the most recent commit message.

**Returns:**

- `str`: Last commit message

**Example:**

```python
from githooks.core.git_operations import get_last_commit_message

msg = get_last_commit_message()
print(f"Last commit: {msg}")
```

##### `is_protected_branch(branch: str) -> bool`

Check if a branch is protected (e.g., `main`, `develop`).

**Parameters:**

- `branch` (str): Branch name to check

**Returns:**

- `bool`: `True` if branch is protected, `False` otherwise

**Example:**

```python
from githooks.core.git_operations import is_protected_branch

if is_protected_branch("main"):
    print("Cannot commit directly to main")
```

##### `get_commit_diff() -> str`

Get the diff of staged changes.

**Returns:**

- `str`: Git diff output

**Example:**

```python
from githooks.core.git_operations import get_commit_diff

diff = get_commit_diff()
if ".pyc" in diff:
    print("Warning: Compiled Python files detected")
```

---

### git_config

Git configuration management.

**Location:** `githooks/core/git_config.py`

#### Functions

##### `get_git_config(key: str, default: Optional[str] = None) -> str`

Get Git configuration value.

**Parameters:**

- `key` (str): Config key (e.g., `user.name`, `hooks.jira.server`)
- `default` (str, optional): Default value if key not found

**Returns:**

- `str`: Configuration value, or `default` if not found

**Raises:**

- `RuntimeError`: If neither key exists nor default is provided

**Example:**

```python
from githooks.core.git_config import get_git_config

email = get_git_config("user.email", default="not-configured")
jira_server = get_git_config("hooks.jira.server")
```

##### `set_git_config(key: str, value: str, global_config: bool = False) -> None`

Set Git configuration value.

**Parameters:**

- `key` (str): Config key
- `value` (str): Config value
- `global_config` (bool): If `True`, set globally; if `False`, set locally for repository

**Raises:**

- `RuntimeError`: If git command fails

**Example:**

```python
from githooks.core.git_config import set_git_config

set_git_config("hooks.jira.server", "https://jira.example.com")
set_git_config("user.email", "dev@example.com", global_config=True)
```

##### `get_user_name() -> str`

Get Git user name.

**Returns:**

- `str`: User name (from `user.name` config)

**Example:**

```python
from githooks.core.git_config import get_user_name

name = get_user_name()
print(f"User: {name}")
```

##### `get_user_email() -> str`

Get Git user email.

**Returns:**

- `str`: User email (from `user.email` config)

**Example:**

```python
from githooks.core.git_config import get_user_email

email = get_user_email()
if not email:
    raise ValueError("user.email not configured")
```

---

### jira_client

JIRA API client and integration.

**Location:** `githooks/core/jira_client.py`

#### Class: `JiraClient`

JIRA API client for issue tracking operations.

**Constructor:**

```python
JiraClient(server: str, username: str, token: str)
```

**Parameters:**

- `server` (str): JIRA server URL (e.g., `https://jira.example.com`)
- `username` (str): JIRA username or email
- `token` (str): JIRA API token or password

**Example:**

```python
from githooks.core.jira_client import JiraClient

client = JiraClient(
    server="https://jira.example.com",
    username="dev@example.com",
    token="your-api-token"
)
```

#### Methods

##### `get_issue(key: str) -> dict`

Fetch JIRA issue details.

**Parameters:**

- `key` (str): Issue key (e.g., `PTEAE-123`)

**Returns:**

- `dict`: Issue data including summary, status, assignee

**Raises:**

- `JiraException`: If issue not found or API error

**Example:**

```python
issue = client.get_issue("PTEAE-123")
print(f"Status: {issue.fields.status.name}")
```

##### `transition_issue(key: str, transition_name: str, comment: Optional[str] = None) -> bool`

Move issue through workflow transition.

**Parameters:**

- `key` (str): Issue key
- `transition_name` (str): Transition name (e.g., `In Progress`, `Done`)
- `comment` (str, optional): Comment to add to issue

**Returns:**

- `bool`: `True` if successful, `False` if transition not available

**Example:**

```python
success = client.transition_issue("PTEAE-123", "In Progress", "Starting work")
if not success:
    print("Transition not available")
```

##### `add_worklog(key: str, time_spent: str, comment: Optional[str] = None) -> bool`

Log work/time to JIRA issue.

**Parameters:**

- `key` (str): Issue key
- `time_spent` (str): Time in JIRA format (e.g., `2h 30m`, `1d`)
- `comment` (str, optional): Comment for work log

**Returns:**

- `bool`: `True` if successful

**Example:**

```python
client.add_worklog("PTEAE-123", "2h 30m", "Implemented feature")
```

#### Function: `parse_ticket_from_branch(branch_name: str) -> Optional[str]`

Extract JIRA ticket from branch name.

**Parameters:**

- `branch_name` (str): Git branch name

**Returns:**

- `str`: Issue key if found (e.g., `PTEAE-123`), or `None`

**Regex Pattern:** `JT_PTEAE-\d+`

**Example:**

```python
from githooks.core.jira_client import parse_ticket_from_branch

ticket = parse_ticket_from_branch("feature/PTEAE-123_add-login")
print(ticket)  # Output: PTEAE-123
```

---

### jira_helpers

JIRA-specific helper utilities.

**Location:** `githooks/core/jira_helpers.py`

#### Functions

##### `get_jira_client() -> JiraClient`

Get authenticated JIRA client from environment or Git config.

**Sources (in order):**

1. Environment variables: `JIRA_USERNAME`, `JIRA_TOKEN`, `JIRA_SERVER`
2. Git config: `hooks.jira.*`
3. Keyring: Secure credential storage

**Returns:**

- `JiraClient`: Authenticated client

**Raises:**

- `RuntimeError`: If credentials not found or invalid

**Example:**

```python
from githooks.core.jira_helpers import get_jira_client

client = get_jira_client()
issue = client.get_issue("PTEAE-123")
```

##### `validate_jira_credentials() -> bool`

Validate JIRA credentials are configured.

**Returns:**

- `bool`: `True` if valid, `False` otherwise

**Example:**

```python
from githooks.core.jira_helpers import validate_jira_credentials

if not validate_jira_credentials():
    print("JIRA not configured")
```

---

### output

Formatted output and logging.

**Location:** `githooks/core/output.py`

#### Functions

##### `log_success(message: str) -> None`

Print success message in green.

**Example:**

```python
from githooks.core.output import log_success

log_success("Hook executed successfully")
```

##### `log_error(message: str) -> None`

Print error message in red.

**Example:**

```python
from githooks.core.output import log_error

log_error("Operation failed")
```

##### `log_warning(message: str) -> None`

Print warning message in yellow.

**Example:**

```python
from githooks.core.output import log_warning

log_warning("This operation may have side effects")
```

##### `log_info(message: str) -> None`

Print info message in blue.

**Example:**

```python
from githooks.core.output import log_info

log_info("Processing...")
```

---

### runtime_detector

Platform and runtime detection.

**Location:** `githooks/core/runtime_detector.py`

#### Class: `RuntimeCache`

Detects and caches Python runtime information.

**Example:**

```python
from githooks.core.runtime_detector import RuntimeCache

cache = RuntimeCache(repo_path="/path/to/repo")
python_exe = cache.get_python_executable()
```

---

### constants

Project-wide constants.

**Location:** `githooks/core/constants.py`

#### Key Constants

```python
# Branch patterns
BRANCH_REGEX = r"JT_PTEAE-\d+"
PROTECTED_BRANCHES = ["main", "develop", "master"]

# JIRA configuration
DEFAULT_JIRA_SERVER = "https://jira.example.com"
JIRA_PROJECT_KEY = "PTEAE"

# Time tracking
WORKLOG_TRANSITION_TIME = "0.25h"  # Default time per branch transition

# Exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_NOT_FOUND = 127
EXIT_INTERRUPTED = 130
```

---

### utils

Generic utility functions.

**Location:** `githooks/core/utils.py`

#### Functions

##### `run_subprocess(command: List[str], cwd: Optional[str] = None) -> Tuple[int, str, str]`

Execute subprocess command.

**Parameters:**

- `command` (List[str]): Command and arguments
- `cwd` (str, optional): Working directory

**Returns:**

- `Tuple[int, str, str]`: Exit code, stdout, stderr

**Example:**

```python
from githooks.core.utils import run_subprocess

code, stdout, stderr = run_subprocess(["git", "status"])
if code != 0:
    print(f"Error: {stderr}")
```

##### `file_contains(file_path: str, search_term: str) -> bool`

Check if file contains term.

**Example:**

```python
from githooks.core.utils import file_contains

if file_contains("README.md", "deprecated"):
    print("Found deprecation notice")
```

---

## Hook Implementations

### jira_transition_worklog

Post-checkout hook: Auto-transitions JIRA issues on branch switch.

**Location:** `githooks/hooks/jira_transition_worklog.py`

**Entry Point:**

```python
from githooks.hooks.jira_transition_worklog import main
main()
```

**Behavior:**

1. Extracts JIRA ticket from branch name
2. Gets authenticated JIRA client
3. Transitions issue to "In Progress"
4. Logs default work time

### jira_add_push_worklog

Pre-push hook: Logs time to JIRA on push.

**Location:** `githooks/hooks/jira_add_push_worklog.py`

**Entry Point:**

```python
from githooks.hooks.jira_add_push_worklog import main
main()
```

**Behavior:**

1. Extracts JIRA ticket from branch
2. Calculates time since last push
3. Adds worklog entry to JIRA
4. Sends push to remote

---

## Error Codes

| Code | Meaning                      | Recovery                                |
| ---- | ---------------------------- | --------------------------------------- |
| 0    | Success                      | N/A                                     |
| 1    | Generic failure              | Check hook output for details           |
| 127  | Command not found            | Install missing dependency              |
| 130  | Interrupted by user (Ctrl+C) | Restart hook or skip                    |
| 2    | Configuration error          | Fix Git config or environment vars      |
| 3    | JIRA error                   | Check JIRA credentials and connectivity |
| 4    | Permission error             | Check file permissions on hooks         |

---

## Performance Considerations

### Subprocess Execution

Each hook execution spawns subprocess calls:

- Git operations: ~10-50ms per call
- JIRA API calls: ~500-2000ms per call (depends on network)
- Bash script startup: ~10-20ms per hook

**Optimization:**

```python
# Cache JIRA client to reuse authentication
jira_client = get_jira_client()  # Once at module load

# Batch API calls when possible
issues = [client.get_issue(key) for key in keys]  # Instead of looping
```

### Memory Usage

- Typical hook execution: ~20-50MB Python process
- JIRA client with caching: ~5-10MB additional

### Caching

The `RuntimeCache` class caches:

- Python executable path
- Platform detection (Windows/macOS/Linux)
- JIRA client instance
- Git config values

---

## Example: Complete Hook Implementation

```python
#!/usr/bin/env python
"""
Example hook: Validate JIRA ticket in commit message.
"""

import sys
from githooks.core.git_config import get_git_config
from githooks.core.jira_client import parse_ticket_from_branch, JiraClient
from githooks.core.output import log_error, log_success

def main():
    """Validate JIRA ticket in branch name."""
    try:
        # Get branch name and ticket
        with open(".git/HEAD", "r") as f:
            ref = f.read().strip()
        branch = ref.split("/")[-1]

        ticket = parse_ticket_from_branch(branch)
        if not ticket:
            log_error(f"Branch '{branch}' must contain JIRA ticket (JT_PTEAE-###)")
            sys.exit(1)

        # Validate ticket exists
        try:
            server = get_git_config("hooks.jira.server")
            username = get_git_config("hooks.jira.username")
            token = get_git_config("hooks.jira.token")

            client = JiraClient(server, username, token)
            issue = client.get_issue(ticket)

            log_success(f"✓ {ticket}: {issue.fields.summary}")
        except Exception as e:
            log_error(f"Failed to validate {ticket}: {e}")
            sys.exit(1)

        sys.exit(0)

    except Exception as e:
        log_error(f"Hook failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## Backward Compatibility

The API maintains backward compatibility across minor versions:

- Function signatures are stable
- New parameters are optional with defaults
- Deprecated features emit warnings but continue to work
- Major version bumps allow breaking changes
