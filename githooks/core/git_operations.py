# Git command wrappers and helpers
import subprocess
from pathlib import Path
from typing import List, Optional


def safe_run_git(
    cmd: List[str], cwd: Optional[Path] = None, check: bool = True, capture_output: bool = True, text: bool = True
) -> subprocess.CompletedProcess:
    """Run a git command safely with error handling.

    Args:
        cmd (List[str]): The git command and arguments as a list.
        cwd (Optional[Path]): The working directory for the command.
        check (bool): Whether to raise an error on non-zero exit.
        capture_output (bool): Whether to capture stdout/stderr.
        text (bool): Whether to decode output as text.
    Returns:
        subprocess.CompletedProcess: The result of the subprocess run.
    Raises:
        RuntimeError: If the command fails.
    """
    try:
        # Always use utf-8 encoding with error replacement for cross-platform unicode support
        if text:
            return subprocess.run(cmd, cwd=cwd, check=check, capture_output=capture_output, encoding="utf-8", errors="replace")
        return subprocess.run(cmd, cwd=cwd, check=check, capture_output=capture_output)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Command '{' '.join(cmd)}' failed: {exc}") from exc


def get_current_branch(repo_path: Optional[Path] = None) -> Optional[str]:
    """Get the current git branch name for the given repository path.

    Args:
        repo_path (Optional[Path]): The path to the git repository.
    Returns:
        Optional[str]: The current branch name, or None if not found.
    """
    cmd = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
    try:
        result = safe_run_git(cmd, cwd=repo_path, check=True)
        return result.stdout.strip() if result.returncode == 0 else None
    except RuntimeError:
        return None


def get_commits_since(base_branch: str, repo_path: Optional[Path] = None) -> List[str]:
    """Get commit messages since the given base branch.

    Args:
        base_branch (str): The base branch to compare against (e.g., 'develop').
        repo_path (Optional[Path]): The path to the git repository.
    Returns:
        List[str]: List of commit messages since the base branch.
    """
    cmd = ["git", "log", f"{base_branch}..HEAD", "--pretty=format:%s"]
    try:
        result = safe_run_git(cmd, cwd=repo_path, check=True)
        if result.returncode == 0:
            return result.stdout.strip().splitlines()
        return []
    except RuntimeError:
        return []
