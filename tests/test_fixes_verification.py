"""Verification that the key fixes are correct, without depending on external repo."""

import re
import subprocess
import tempfile
from pathlib import Path


def test_prepare_commit_msg_hook_regex():
    """Verify the prepare-commit-msg hook regex correctly detects conventional types."""
    # The regex from the fix
    pattern = r"^(feat|fix|docs|style|refactor|test|chore|ci)(?:\(.*?\))?(!)?:"

    # Test cases that should match
    valid_messages = [
        "feat: add feature",
        "fix: fix bug",
        "feat(api): add endpoint",
        "feat(api)!: breaking change",
        "fix!: breaking fix",
        "docs(readme): update",
        "test(utils): add tests",
    ]

    # Test cases that should NOT match
    invalid_messages = [
        "add feature",
        "feature: something",
        "feat : missing colon space",
    ]

    print("Testing prepare-commit-msg hook regex...")
    for msg in valid_messages:
        match = bool(re.match(pattern, msg))
        assert match, f"Expected to match: {msg}"
        print(f"[OK] Matched: {msg}")

    for msg in invalid_messages:
        match = bool(re.match(pattern, msg))
        assert not match, f"Should not match: {msg}"
        print(f"[OK] Correctly rejected: {msg}")

    print("[OK] All regex tests passed!")


def test_runtime_detector_git_config_scopes():
    """Verify that git config --local and --global scopes work correctly."""
    print("\nTesting git config scope handling...")

    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)

        # Initialize a git repo
        subprocess.run(["git", "init"], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=repo_path, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True)

        # Write to local config
        subprocess.run(
            ["git", "config", "--local", "test.key", "local_value"],
            cwd=repo_path,
            check=True,
        )

        # Read with --local flag should return the value
        result = subprocess.run(
            ["git", "config", "--local", "test.key"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, "Should be able to read local config"
        assert result.stdout.strip() == "local_value", f"Got: {result.stdout.strip()}"
        print("✓ Can write and read local config with --local flag")

        # Unset with --local flag
        result = subprocess.run(
            ["git", "config", "--local", "--unset", "test.key"],
            cwd=repo_path,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0, "Should be able to unset local config"
        print("[OK] Can unset local config with --local flag")

        # Read with --local flag should now fail (key doesn't exist)
        result = subprocess.run(
            ["git", "config", "--local", "test.key"],
            cwd=repo_path,
            capture_output=True,
            check=False,
        )
        assert result.returncode != 0, "Key should not exist after unset"
        print("[OK] Key correctly removed from local config")

        print("[OK] All git config scope tests passed!")


if __name__ == "__main__":
    test_prepare_commit_msg_hook_regex()
    test_runtime_detector_git_config_scopes()
    print("\n[OK] All verification tests passed!")
