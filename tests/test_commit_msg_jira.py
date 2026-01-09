"""
Tests for commit-msg-jira hook.

Verifies existence and execution of the commit-msg-jira hook script.
"""

import os
import subprocess
import sys
import tempfile

import pytest

HOOK_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "commit-msg", "commit-msg-jira"))


def to_bash_path(path: str) -> str:
    """Convert Windows path to Bash-compatible path for Git Bash."""
    if sys.platform.startswith("win"):
        # Try cygpath if available
        try:
            result = subprocess.run(["cygpath", "-u", path], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except Exception:
            # Manual conversion: C:\Users\foo -> /c/Users/foo
            drive, rest = os.path.splitdrive(path)
            drive = drive.rstrip(":\\/")
            rest = rest.replace("\\", "/")
            return f"/{drive.lower()}{rest}"
    return path


def test_hook_exists():
    """Hook script should exist in commit-msg directory."""
    assert os.path.isfile(HOOK_PATH)


def test_hook_executable():
    """Hook script should be executable and return 0 or 1 for valid/invalid commit messages."""
    if not os.path.isfile(HOOK_PATH):
        pytest.skip("Hook script not found; skipping test.")
    # Check if running on Windows and if git is available in Bash
    if sys.platform.startswith("win"):
        git_check = subprocess.run(["bash", "-c", "which git"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if git_check.returncode != 0:
            pytest.skip("Bash or git not available in test environment; skipping test.")
    bash_hook_path = to_bash_path(HOOK_PATH)
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write("JT_PTEAE-1234: add feature")
        f.flush()
        result = subprocess.run(["bash", bash_hook_path, f.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        assert result.returncode in (0, 1)
    os.unlink(f.name)


@pytest.mark.parametrize(
    "msg,expected",
    [
        ("JT_PTEAE-1234: add feature", 0),
        ("no ticket in message", 1),
    ],
)
def test_hook_validates_jira_ticket(msg: str, expected: int) -> None:
    """Hook should validate presence of JIRA ticket in commit message."""
    if not os.path.isfile(HOOK_PATH):
        pytest.skip("Hook script not found; skipping test.")
    if sys.platform.startswith("win"):
        git_check = subprocess.run(["bash", "-c", "which git"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if git_check.returncode != 0:
            pytest.skip("Bash or git not available in test environment; skipping test.")
    bash_hook_path = to_bash_path(HOOK_PATH)
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write(msg)
        f.flush()
        result = subprocess.run(["bash", bash_hook_path, f.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        assert result.returncode == expected
    os.unlink(f.name)
