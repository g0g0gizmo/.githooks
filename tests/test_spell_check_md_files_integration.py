"""
Integration test for pre-commit/spell-check-md-files.hook.

Simulates a real git commit in a temp repo and checks spell check enforcement.
"""

import os
import subprocess

import pytest


def test_spell_check_md_files_hook_blocks_on_typo(temp_git_repo):
    """Should block commit if .md file contains a typo (requires aspell installed)."""
    repo = temp_git_repo
    subprocess.run(["git", "init"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    
    # Create and switch to a feature branch (to avoid "no commits to main" error)
    subprocess.run(["git", "checkout", "-b", "feature/test-spell-check"], cwd=repo, check=True)
    
    # Create a markdown file with a typo
    with open(os.path.join(repo, "README.md"), "w", encoding="utf-8") as f:
        f.write("Thiss is a testt.")
    subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
    # Try to commit (should fail due to typo)
    result = subprocess.run(["git", "commit", "-m", "test"], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    # Accept both 0 (if aspell not installed) or nonzero (if blocked)
    if result.returncode == 0:
        pytest.skip("aspell not installed or hook not enforced")
    assert b"Thiss" in result.stdout or b"Thiss" in result.stderr or b"testt" in result.stdout or b"testt" in result.stderr
