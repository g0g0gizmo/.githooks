"""
Utility functions for git-go workflow automation.

This module provides common utility functions including error handling,
dependency management, and Git operations wrappers.
"""

import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from githooks.core.constants import REQUIRED_DEPENDENCIES
from githooks.core.git_operations import safe_run_git


# Custom exception for graceful error handling
class GitGoError(Exception):
    """Custom exception for git-go workflow errors."""


# Configure logging for all scripts that import utils
LOG_LEVEL = os.environ.get("GIT_GO_LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO), format="[%(levelname)s] %(message)s")
logger = logging.getLogger("git-go")


def push_latest_changes(repo_path: Path, branch_name: str, current_branch: Optional[str] = None) -> None:
    """
    Push latest changes to remote for the given branch.

    Args:
        repo_path (Path): Path to the git repository root.
        branch_name (str): Name of the branch to push.
        current_branch (Optional[str]): Current branch name (optional).

    Raises:
        GitGoError: If the push operation fails.
    """
    if not current_branch or branch_name not in (current_branch or ""):
        logger.warning("Current branch '%s' doesn't match expected '%s'", current_branch, branch_name)
    logger.info("Pushing latest changes...")
    try:
        safe_run_git(["git", "push", "origin", current_branch or branch_name], cwd=repo_path, check=True, capture_output=True)
        logger.info("Changes pushed to remote")
    except RuntimeError as e:
        logger.error("Failed to push changes: %s", e)
        raise GitGoError(f"Failed to push changes: {e}") from e


def ensure_dependencies() -> None:
    """
    Check for required dependencies and install if missing.

    Raises:
        GitGoError: If dependencies cannot be installed.
    """
    missing: List[str] = []
    for module, package in REQUIRED_DEPENDENCIES.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    if missing:
        logger.info("Installing missing dependencies: %s", ", ".join(missing))
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet"] + missing, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.info("Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            logger.error("Failed to install dependencies: %s", e)
            raise GitGoError(f"Failed to install dependencies: {e}") from e
