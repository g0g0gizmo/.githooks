"""
Pytest configuration and shared fixtures for Git hooks tests.

Provides common fixtures for testing Git hooks including temporary Git repositories,
mock Jira clients, and environment setup/teardown.
"""

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Generator, List

import pytest

# Import shared constants/utilities for use in tests
from githooks.core.constants import BRANCH_REGEX, DEFAULT_JIRA_SERVER, SERVICE_NAME
from githooks.core.git_config import get_git_config, set_git_config
from githooks.core.git_operations import get_current_branch, safe_run_git
from githooks.core.jira_client import get_jira_client, parse_ticket_from_branch

# Real test repository URL - all tests should use this
REAL_TEST_REPO_URL = "https://git.viasat.com/jtuttle/test-repo"
REAL_TEST_REPO_BRANCHES_URL = f"{REAL_TEST_REPO_URL}/branches"
REAL_TEST_JIRA_TICKET = "OMLEG-3270"


@pytest.fixture(scope="session", autouse=True)
def update_global_githooks():
    """
    Updates global githooks before test session starts.

    This ensures the global hook installation is current, though most tests
    will install hooks locally in their test repositories (see temp_git_repo
    and real_test_repo fixtures which copy and install hooks for each test).

    Runs once per test session (autouse=True, scope="session").
    """
    # Get the path to install.py (in project root)
    project_root = Path(__file__).parent.parent
    install_script = project_root / "install.py"

    if not install_script.exists():
        pytest.fail(f"install.py not found at {install_script}")

    print(f"\n{'='*70}")
    print("Updating global githooks before test session...")
    print(f"Note: Test repos will also install hooks locally with current code")
    print(f"{'='*70}")

    try:
        # Run install.py with --global flag to update global hooks
        result = subprocess.run(
            [sys.executable, str(install_script), "--global", "--force"], capture_output=True, text=True, check=False, cwd=str(project_root)
        )

        if result.returncode == 0:
            print("[OK] Global githooks updated successfully")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"[WARNING] Global githooks update failed (exit code {result.returncode})")
            if result.stderr:
                print(f"Error: {result.stderr}")
            # Don't fail the test session - some environments may not support global hooks

    except Exception as e:
        print(f"[WARNING] Failed to update global githooks: {e}")
        # Don't fail the test session - continue with existing hooks

    print(f"{'='*70}\n")

    yield  # Run tests

    # No cleanup needed - global hooks remain installed for development use


# Fixture to track and cleanup Jira worklogs created during tests
@pytest.fixture
def jira_worklog_cleanup():
    """
    Tracks Jira worklogs created during a test and deletes them on cleanup.

    Usage:
        worklog_ids = []
        ...
        # After creating a worklog via Jira API:
        worklog_ids.append((issue_key, worklog_id))
        ...
        # Register for cleanup
        request.getfixturevalue('jira_worklog_cleanup').register(issue_key, worklog_id, jira_client)
    """
    worklogs = []  # List of (issue_key, worklog_id, jira_client)

    def register(issue_key, worklog_id, jira_client):
        worklogs.append((issue_key, worklog_id, jira_client))

    yield type("WorklogCleanup", (), {"register": register})

    # Cleanup: delete all registered worklogs
    for issue_key, worklog_id, jira_client in worklogs:
        try:
            jira_client.delete_worklog(issue_key, worklog_id)
        except Exception as e:
            print(f"Warning: Failed to delete Jira worklog {worklog_id} for {issue_key}: {e}")


@pytest.fixture
def load_hook_module():
    """
    Load a .hook file as a Python module for testing.
    Usage:
        hook = load_hook_module(path_to_hook)
        hook.main()  # or whatever entry point
    """

    def _loader(hook_path):
        spec = importlib.util.spec_from_file_location("hook_module", hook_path)
        if spec is None:
            raise ImportError(f"Cannot create module spec from {hook_path}")
        hook_module = importlib.util.module_from_spec(spec)
        loader = spec.loader
        if loader is not None:
            loader.exec_module(hook_module)
        else:
            raise ImportError(f"Cannot load module from {hook_path}")
        return hook_module

    return _loader


@pytest.fixture
def temp_git_repo() -> Generator[Path, None, None]:
    """
    DEPRECATED: Use real_test_repo instead.

    This fixture now redirects to the real test repository to ensure
    all tests run against the configured test repository (REAL_TEST_REPO_URL)

    Yields:
        Path: Path to the cloned real test repository
    """
    # Track branches created during this test for cleanup
    created_branches: List[str] = []

    # Clone the real test repository
    temp_dir = tempfile.mkdtemp(prefix="test_repo_clone_")
    repo_path = Path(temp_dir)

    try:
        # Clone the repository with error handling
        result = subprocess.run(["git", "clone", REAL_TEST_REPO_URL, str(repo_path)], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            pytest.skip(f"Cannot access test repository {REAL_TEST_REPO_URL} (network error or access denied)")

        # Verify clone was successful
        if not (repo_path / ".git").exists():
            pytest.skip(f"Failed to clone {REAL_TEST_REPO_URL}: .git directory not found")

        # Configure local user for commits
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test.user@example.com"], cwd=repo_path, check=True, capture_output=True)

        # Copy install.py and all hook directories from project root to test repo
        project_root = Path(__file__).parent.parent
        shutil.copy2(project_root / "install.py", repo_path / "install.py")

        # Copy all hook directories (pre-commit, commit-msg, post-checkout, etc.)
        for hook_dir in project_root.glob("*"):
            if hook_dir.is_dir() and (hook_dir / "dispatcher.hook").exists() or any(hook_dir.glob("*.hook")):
                dest_dir = repo_path / hook_dir.name
                if dest_dir.exists():
                    shutil.rmtree(dest_dir)
                shutil.copytree(hook_dir, dest_dir)

        # Also copy githooks module for hook dependencies
        if (project_root / "githooks").exists():
            shutil.copytree(project_root / "githooks", repo_path / "githooks", dirs_exist_ok=True)

        # Install hooks locally in this test repo (uses copied files)
        install_result = subprocess.run(
            [sys.executable, str(repo_path / "install.py"), "--force"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=30,
        )
        # Log installation result but don't fail if hooks can't install (missing deps OK)
        if install_result.returncode != 0:
            print(f"⚠ Hook installation warning in test repo: {install_result.stderr}")

        # Get the initial branch to track what branches we create
        result = subprocess.run(["git", "branch", "--show-current"], cwd=repo_path, capture_output=True, text=True, check=True)
        initial_branch = result.stdout.strip()

        # Yield the repo path to the test
        yield repo_path

        # CLEANUP: Find all local branches that aren't the initial branch
        result = subprocess.run(["git", "branch", "--format=%(refname:short)"], cwd=repo_path, capture_output=True, text=True, check=True)
        all_branches = [b.strip() for b in result.stdout.strip().split("\n") if b.strip()]
        created_branches = [b for b in all_branches if b != initial_branch]

        # Rename all created branches with DELETE suffix and push
        for branch in created_branches:
            try:
                # Switch to initial branch if we're on the branch to be renamed
                current = subprocess.run(["git", "branch", "--show-current"], cwd=repo_path, capture_output=True, text=True, check=True).stdout.strip()

                if current == branch:
                    subprocess.run(["git", "checkout", initial_branch], cwd=repo_path, capture_output=True, check=True)

                # Rename branch locally with DELETE suffix
                new_name = f"{branch}_DELETE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                subprocess.run(["git", "branch", "-m", branch, new_name], cwd=repo_path, capture_output=True, check=True)

                # Delete old branch from remote if it exists
                subprocess.run(["git", "push", "origin", "--delete", branch], cwd=repo_path, capture_output=True, timeout=30)

                # Push renamed branch to remote for manual deletion
                subprocess.run(["git", "push", "-u", "origin", new_name], cwd=repo_path, capture_output=True, timeout=30)

                print(f"✓ Renamed and pushed branch '{branch}' -> '{new_name}' for manual deletion")

            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                print(f"⚠ Warning: Failed to cleanup branch '{branch}': {e}")

    except subprocess.TimeoutExpired:
        pytest.skip(f"Timeout cloning {REAL_TEST_REPO_URL} - network issue or repository unavailable")
    except subprocess.CalledProcessError as e:
        pytest.skip(f"Failed to clone {REAL_TEST_REPO_URL}: {e.stderr if hasattr(e, 'stderr') else str(e)}")
    except Exception as e:
        pytest.skip(f"Unexpected error with test repository: {e}")
    finally:
        # Always cleanup the local clone
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def real_test_repo() -> Generator[Path, None, None]:
    """
    Clone the real test repository for integration testing.

    All tests should use this fixture instead of creating temporary repos.
    Uses the configured test repository (REAL_TEST_REPO_URL) which should be
    configured in global Git config with appropriate credentials.

    After test completion, automatically renames all created branches with
    a DELETE suffix and pushes them to remote for manual deletion later.

    Yields:
        Path: Path to the cloned real test repository
    """
    # Track branches created during this test for cleanup
    created_branches: List[str] = []

    # Clone the real test repository
    temp_dir = tempfile.mkdtemp(prefix="test_repo_clone_")
    repo_path = Path(temp_dir)

    try:
        # Clone the repository with error handling
        result = subprocess.run(["git", "clone", REAL_TEST_REPO_URL, str(repo_path)], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            pytest.skip(f"Cannot access test repository {REAL_TEST_REPO_URL} (network error or access denied)")

        # Verify clone was successful
        if not (repo_path / ".git").exists():
            pytest.skip(f"Failed to clone {REAL_TEST_REPO_URL}: .git directory not found")

        # Configure local user for commits
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test.user@example.com"], cwd=repo_path, check=True, capture_output=True)

        # Copy install.py and all hook directories from project root to test repo
        project_root = Path(__file__).parent.parent
        shutil.copy2(project_root / "install.py", repo_path / "install.py")

        # Copy all hook directories (pre-commit, commit-msg, post-checkout, etc.)
        for hook_dir in project_root.glob("*"):
            if hook_dir.is_dir() and (hook_dir / "dispatcher.hook").exists() or any(hook_dir.glob("*.hook")):
                dest_dir = repo_path / hook_dir.name
                if dest_dir.exists():
                    shutil.rmtree(dest_dir)
                shutil.copytree(hook_dir, dest_dir)

        # Also copy githooks module for hook dependencies
        if (project_root / "githooks").exists():
            shutil.copytree(project_root / "githooks", repo_path / "githooks", dirs_exist_ok=True)

        # Install hooks locally in this test repo (uses copied files)
        install_result = subprocess.run(
            [sys.executable, str(repo_path / "install.py"), "--force"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=30,
        )
        # Log installation result but don't fail if hooks can't install (missing deps OK)
        if install_result.returncode != 0:
            print(f"⚠ Hook installation warning in test repo: {install_result.stderr}")

        # Get the initial branch to track what branches we create
        result = subprocess.run(["git", "branch", "--show-current"], cwd=repo_path, capture_output=True, text=True, check=True)
        initial_branch = result.stdout.strip()

        # Yield the repo path to the test
        yield repo_path

        # CLEANUP: Find all local branches that aren't the initial branch
        result = subprocess.run(["git", "branch", "--format=%(refname:short)"], cwd=repo_path, capture_output=True, text=True, check=True)
        all_branches = [b.strip() for b in result.stdout.strip().split("\n") if b.strip()]
        created_branches = [b for b in all_branches if b != initial_branch]

        # Rename all created branches with DELETE suffix and push
        for branch in created_branches:
            try:
                # Switch to initial branch if we're on the branch to be renamed
                current = subprocess.run(["git", "branch", "--show-current"], cwd=repo_path, capture_output=True, text=True, check=True).stdout.strip()

                if current == branch:
                    subprocess.run(["git", "checkout", initial_branch], cwd=repo_path, capture_output=True, check=True)

                # Rename branch locally with DELETE suffix
                new_name = f"{branch}_DELETE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                subprocess.run(["git", "branch", "-m", branch, new_name], cwd=repo_path, capture_output=True, check=True)

                # Delete old branch from remote if it exists
                subprocess.run(["git", "push", "origin", "--delete", branch], cwd=repo_path, capture_output=True, timeout=30)

                # Push renamed branch to remote for manual deletion
                subprocess.run(["git", "push", "-u", "origin", new_name], cwd=repo_path, capture_output=True, timeout=30)

                print(f"✓ Renamed and pushed branch '{branch}' -> '{new_name}' for manual deletion")

            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                print(f"⚠ Warning: Failed to cleanup branch '{branch}': {e}")

    except subprocess.TimeoutExpired:
        pytest.skip(f"Timeout cloning {REAL_TEST_REPO_URL} - network issue or repository unavailable")
    except subprocess.CalledProcessError as e:
        pytest.skip(f"Failed to clone {REAL_TEST_REPO_URL}: {e.stderr if hasattr(e, 'stderr') else str(e)}")
    except Exception as e:
        pytest.skip(f"Unexpected error with test repository: {e}")
    finally:
        # Always cleanup the local clone
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def clean_env():
    """
    Provide a clean environment without Jira credentials.
    Saves current environment variables and restores them after the test.
    """
    original_env = os.environ.copy()
    # Remove Jira-related environment variables
    jira_keys = ["JIRA_USERNAME", "JIRA_TOKEN", "JIRA_SERVER", "GOJIRA_USERNAME", "GOJIRA_SECRET"]
    for key in jira_keys:
        os.environ.pop(key, None)
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_jira_env():
    """
    Provide mock Jira environment variables for testing.

    Sets up test credentials that won't interact with real Jira.
    """
    original_env = os.environ.copy()

    os.environ["JIRA_USERNAME"] = "test_user@example.com"
    os.environ["JIRA_TOKEN"] = "test_token_12345"
    os.environ["JIRA_SERVER"] = "https://test.jira.com"

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def sample_branches():
    """
    Provide sample Git branch names for testing.

    Returns:
        dict: Dictionary of branch names with expected ticket IDs
    """
    return {
        "feature/PROJ-123-add-feature": "PROJ-123",
        "bugfix/ABC-456-fix-bug": "ABC-456",
        "JT_PTEAE-2930_automatic-sw-versioning": "PTEAE-2930",
        "develop-feature/JT_OMLEG-3169_reverse_proxy": "OMLEG-3169",
        "main": "main",
        "develop": "develop",
        "no-ticket-branch": "no-ticket-branch",
        "feature/add-something": "feature/add-something",
    }
