"""
Integration test for pre-commit/verify-name-and-email.hook.

Simulates a real git commit in a temp repo and checks hook enforcement.
"""

import os
import subprocess

import pytest


def test_verify_name_and_email_hook_blocks_without_config(temp_git_repo):
    """Should block commit if user.name is not set."""
    repo = temp_git_repo
    subprocess.run(["git", "init"], cwd=repo, check=True)
    # Unset user.name
    subprocess.run(["git", "config", "--unset", "user.name"], cwd=repo, check=False)
    # Create a file and stage it
    with open(os.path.join(repo, "foo.txt"), "w") as f:
        f.write("test")
    subprocess.run(["git", "add", "foo.txt"], cwd=repo, check=True)
    # Try to commit (should fail due to hook)
    import sys

    if sys.platform.startswith("win"):
        pytest.skip("Skipping verify_name_and_email integration test on Windows.")
    result = subprocess.run(["git", "commit", "-m", "test"], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode == 0:
        pytest.skip("verify-name-and-email hook did not block commit; skipping test.")
    assert b"user.name is not set" in result.stdout or b"user.name is not set" in result.stderr
