"""Debug script for test_actual_branch_extract_ticket_from_branch."""
import subprocess
from pathlib import Path
import tempfile
import shutil
import sys
from githooks.cli.commitmint import get_current_branch, extract_ticket_from_branch
import os

# Simplified version of real_test_repo setup
REAL_TEST_REPO_URL = "https://github.com/jtuttle-personal/test-repo.git"

temp_dir = tempfile.mkdtemp(prefix="test_repo_clone_")
repo_path = Path(temp_dir)

try:
    # Clone the repository
    subprocess.run(["git", "clone", REAL_TEST_REPO_URL, str(repo_path)], check=True, capture_output=True, text=True, timeout=30)

    # Configure local user for commits
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test.user@example.com"], cwd=repo_path, check=True, capture_output=True)

    # Get current branch
    current_branch = get_current_branch(repo_path)
    print(f"Current branch: {repr(current_branch)}")

    # Now try to do the test
    initial_branch = current_branch
    print(f"Initial branch: {repr(initial_branch)}")

    if not initial_branch:
        print("ERROR: initial_branch is None or empty!")
        # Debug: check git status
        result = subprocess.run(["git", "status"], cwd=repo_path, capture_output=True, text=True)
        print("Git status:")
        print(result.stdout)
        sys.exit(1)

    # Create a test branch
    test_branch = "JT_ISSUE-1234_test_feature"
    subprocess.run(["git", "checkout", "-b", test_branch], cwd=repo_path, check=True, capture_output=True)
    print(f"Created and switched to: {test_branch}")

    # Try to switch back
    print(f"Trying to switch back to: {initial_branch}")
    result = subprocess.run(["git", "checkout", str(initial_branch)], cwd=repo_path, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        print(f"Checking what branches exist:")
        result = subprocess.run(["git", "branch", "-a"], cwd=repo_path, capture_output=True, text=True)
        print(result.stdout)
    else:
        print("Successfully switched back")

finally:
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)
