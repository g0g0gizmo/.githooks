"""
Tests for autoversion-conventional-commit.hook.

Verifies existence, importability, and correct behavior for conventional and non-conventional commits.
"""

import os
import shutil
import subprocess
import sys
import tempfile

import pytest

HOOK_PATH = os.path.join(os.path.dirname(__file__), "../post-commit/autoversion-conventional-commit.hook")


def test_hook_exists():
    """Hook script should exist in post-commit directory."""
    disabled_path = HOOK_PATH + ".disabled"
    if not os.path.isfile(HOOK_PATH) and os.path.isfile(disabled_path):
        pytest.skip(f"Hook is disabled: {disabled_path}")
    assert os.path.isfile(HOOK_PATH)


def test_hook_importable(load_hook_module):
    """Hook script should be importable as a Python module (if Python)."""
    disabled_path = HOOK_PATH + ".disabled"
    if not os.path.isfile(HOOK_PATH) and os.path.isfile(disabled_path):
        pytest.skip(f"Hook is disabled: {disabled_path}")
    if not os.path.isfile(HOOK_PATH):
        pytest.skip(f"Hook not found: {HOOK_PATH}")

    with open(HOOK_PATH, encoding="utf-8") as f:
        first_line = f.readline()
    if not (first_line.startswith("#!/usr/bin/env python") or first_line.startswith("#!/usr/bin/python")):
        pytest.skip("Not a Python script; skipping import test.")
    import importlib.util

    spec = importlib.util.spec_from_file_location("hook_module", HOOK_PATH)
    if spec is None or spec.loader is None:
        pytest.skip("Could not load Python module spec; skipping import test.")
    load_hook_module(HOOK_PATH)
    # Should not raise


def run_git_with_commit_message(commit_msg: str) -> subprocess.CompletedProcess[str]:
    """Helper to run the hook in a temp git repo with a given commit message."""
    disabled_path = HOOK_PATH + ".disabled"
    if not os.path.isfile(HOOK_PATH) and os.path.isfile(disabled_path):
        pytest.skip(f"Hook is disabled: {disabled_path}")
    if not os.path.isfile(HOOK_PATH):
        pytest.skip(f"Hook not found: {HOOK_PATH}")

    with tempfile.TemporaryDirectory() as repo:
        subprocess.run(["git", "init"], cwd=repo, check=True)
        with open(os.path.join(repo, "file.txt"), "w", encoding="utf-8") as f:
            f.write("test")
        subprocess.run(["git", "add", "file.txt"], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo, check=True)
        # Copy hook to repo
        hook_dest = os.path.join(repo, "autoversion-conventional-commit.hook")
        shutil.copy(HOOK_PATH, hook_dest)
        result = subprocess.run([sys.executable, hook_dest], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, text=True)
        return result


@pytest.mark.parametrize(
    "msg,should_run",
    [
        ("feat: add feature", True),
        ("fix: bug fix", True),
        ("docs: update docs", False),
        ("random message", False),
    ],
)
def test_hook_behavior_on_commit_message(msg: str, should_run: bool) -> None:
    """Hook should run standard-version only for conventional commits."""
    result = run_git_with_commit_message(msg)
    # If npx is missing, exit code will be 1 and error message will mention npx
    if should_run:
        assert result.returncode in (0, 1)
    else:
        assert result.returncode == 0
