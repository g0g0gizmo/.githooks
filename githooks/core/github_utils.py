"""
Git operations helper functions for git-go commands.

This module contains all Git-related operations including branch management,
cloning, pushing, and status checks.
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Any, List, Optional

from github import Github  # type: ignore[import,no-redef]

from githooks.core.constants import BRANCH_REGEX, DEFAULT_JIRA_SERVER
from githooks.core.git_operations import get_commits_since as lib_get_commits_since
from githooks.core.git_operations import get_current_branch as lib_get_current_branch
from githooks.core.repo_helpers import build_pr_body, get_github_token, get_repo_from_url  # type: ignore[attr-defined]
from githooks.core.utils import push_latest_changes


def safe_run(
    cmd: List[str], cwd: Optional[Path] = None, check: bool = False, capture_output: bool = True, text: bool = False
) -> subprocess.CompletedProcess[Any]:
    """Run subprocess command with standardized error handling.

    Returns subprocess.CompletedProcess on success; raises RuntimeError on failure.
    """
    try:
        # Always use utf-8 encoding with error replacement when text mode is enabled
        if text:
            return subprocess.run(cmd, cwd=cwd, check=check, capture_output=capture_output, encoding="utf-8", errors="replace")  # type: ignore[arg-type]
        return subprocess.run(cmd, cwd=cwd, check=check, capture_output=capture_output, text=text)  # type: ignore[arg-type]
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Command '{' '.join(cmd)}' failed: {exc.stderr.decode() if exc.stderr else exc}") from exc


def get_current_branch(repo_path: Path) -> Optional[str]:
    """Delegate to lib.git_operations.get_current_branch to avoid duplication."""
    return lib_get_current_branch(repo_path)


def get_commits_since_branch(repo_path: Path, base_branch: str) -> List[str]:
    """Delegate to lib.git_operations.get_commits_since to avoid duplication."""
    return lib_get_commits_since(base_branch, repo_path)


def get_ticket_from_branch(branch_name: str) -> str:
    """Extract the JIRA ticket from a branch name using BRANCH_REGEX.

    Args:
        branch_name: Git branch name

    Returns:
        JIRA ticket identifier

    Raises:
        SystemExit if ticket cannot be found
    """
    ticket_match = re.search(BRANCH_REGEX, branch_name)
    if not ticket_match:
        print(f"[ERROR] No JIRA ticket found in branch name: {branch_name}", file=sys.stderr)
        sys.exit(1)
    return ticket_match.group(1)


def extract_ticket_from_branch(branch_name: str) -> Optional[str]:
    """Extract JIRA ticket from branch name. Returns None if not found.

    Args:
        branch_name: Git branch name

    Returns:
        JIRA ticket identifier or None
    """
    ticket_match = re.search(BRANCH_REGEX, branch_name)
    return ticket_match.group(1) if ticket_match else None


def get_user_initials() -> str:
    """Get user initials from Git configuration.

    Returns:
        User initials (first letters of name parts, reversed if more than one part)
    """
    try:
        result = subprocess.run(["git", "config", "user.name"], capture_output=True, check=False, encoding="utf-8", errors="replace")
        name = result.stdout.strip()
        parts = [part[0].upper() for part in name.split() if part]
        # Reverse order to handle "Last First" format (e.g., "Tuttle John" -> "JT")
        return "".join(reversed(parts)) if len(parts) > 1 else "".join(parts)
    except (OSError, subprocess.SubprocessError):
        return "XX"


def format_summary_for_branch(summary: str, max_length: int = 50) -> str:
    """Format a JIRA issue summary for use in a branch name.

    Args:
        summary: JIRA issue summary text
        max_length: Maximum length for the formatted summary

    Returns:
        Formatted summary suitable for branch name
    """
    summary = summary.strip().lower()
    summary = re.sub(r"[^a-z0-9]+", "_", summary)
    summary = re.sub(r"_+", "_", summary)
    summary = summary.strip("_")
    if len(summary) <= max_length:
        return summary
    words = summary.split("_")
    result: list[str] = []
    current_length = 0
    for word in words:
        if current_length + len(word) + 1 > max_length:
            break
        result.append(word)
        current_length += len(word) + 1
    return "_".join(result) if result else summary[:max_length]


def create_branch_name(jira_ticket: str, summary: str, branch_prefix: str = "", root_branch: str = "develop") -> str:  # type: ignore[misc]
    """Create a Git branch name from JIRA ticket and summary.

    Args:
        jira_ticket: JIRA ticket identifier
        summary: JIRA issue summary
        branch_prefix: Optional prefix (e.g., 'feature/')
        root_branch: Root branch name (not used in current implementation)

    Returns:
        Formatted branch name
    """
    _ = root_branch  # Suppress unused parameter warning
    initials = get_user_initials()
    formatted_summary = format_summary_for_branch(summary)
    base_name = f"{initials}_{jira_ticket.upper()}_{formatted_summary}"
    if branch_prefix:
        if not branch_prefix.endswith("/"):
            branch_prefix += "/"
        return f"{branch_prefix}{base_name}"
    return base_name


def clone_or_update_repo(url: str, clone_to: str, root_branch: str, branch_name: str) -> Path:
    """Clone a repository or update existing clone.

    Args:
        url: Git repository URL
        clone_to: Base directory for clones
        root_branch: Root branch to use
        branch_name: Branch name for directory naming

    Returns:
        Path to the repository directory
    """
    dir_name = branch_name.split("/")[-1] if "/" in branch_name else branch_name
    base_path = Path(clone_to)
    repo_path = base_path / dir_name
    git_dir = repo_path / ".git"
    if git_dir.exists():
        print(f"[INFO] Repository exists at {repo_path}, updating...")
        subprocess.run(["git", "fetch", "origin"], cwd=repo_path, check=True)
        subprocess.run(["git", "checkout", root_branch], cwd=repo_path, check=True)
        subprocess.run(["git", "pull", "origin", root_branch], cwd=repo_path, check=True)
        print(f"[OK] Updated {root_branch} branch")
    elif repo_path.exists():
        print(f"[ERROR] Directory {repo_path} exists but is not a git repository", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"[INFO] Cloning repository to {repo_path}...")
        base_path.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", url, str(repo_path)], check=True)
        subprocess.run(["git", "checkout", root_branch], cwd=repo_path, check=True)
        subprocess.run(["git", "pull", "origin", root_branch], cwd=repo_path, check=True)
        print("[OK] Cloned repository")
    return repo_path


def create_and_push_branch(repo_path: Path, branch_name: str, root_branch: str, max_retries: int = 3) -> bool:
    """Create a new Git branch and push to remote with retry logic.

    This function handles transient network errors and authentication issues by retrying
    the push operation up to max_retries times with exponential backoff.

    Args:
        repo_path: Path to the Git repository
        branch_name: Name for the new branch
        root_branch: Base branch to create from
        max_retries: Maximum number of push attempts (default: 3)

    Returns:
        True if successful, False otherwise

    Error Handling:
        - Transient errors (network timeout, connection refused): Retried with backoff
        - Authentication errors: Logged but not retried (user intervention needed)
        - Branch already exists: Considered success
    """
    import time

    try:
        print(f"[INFO] Creating branch {branch_name}...")
        result_verify = subprocess.run(
            ["git", "rev-parse", "--verify", branch_name],
            cwd=repo_path,
            capture_output=True,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
        if result_verify.returncode == 0:
            print(f"[WARNING] Branch {branch_name} already exists locally")
            subprocess.run(["git", "checkout", branch_name], cwd=repo_path, check=True)
        else:
            subprocess.run(["git", "checkout", root_branch], cwd=repo_path, check=True)
            subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo_path, check=True)
            print(f"[OK] Created branch {branch_name}")

        print("[INFO] Pushing branch to remote...")

        # Retry logic for push operation
        for attempt in range(1, max_retries + 1):
            result_push = subprocess.run(
                ["git", "push", "-u", "origin", branch_name],
                cwd=repo_path,
                capture_output=True,
                check=False,
                encoding="utf-8",
                errors="replace",
            )

            if result_push.returncode == 0:
                print("[OK] Pushed branch to remote")
                return True

            # Check for known success conditions
            stderr_lower = result_push.stderr.lower() if result_push.stderr else ""
            stdout_lower = result_push.stdout.lower() if result_push.stdout else ""
            combined = stderr_lower + stdout_lower

            if ("already exists" in combined) or ("up-to-date" in combined) or ("rejected" in combined and "fast-forward" in combined):
                print("[OK] Branch already exists on remote or is up-to-date")
                return True

            # Determine if error is transient and retryable
            transient_errors = [
                "connection refused",
                "connection reset",
                "timeout",
                "network is unreachable",
                "temporary failure",
                "ssh_exchange_identification",
            ]
            is_transient = any(err in stderr_lower for err in transient_errors)

            if is_transient and attempt < max_retries:
                wait_time = 2 ** (attempt - 1)  # Exponential backoff: 1s, 2s, 4s
                print(f"[WARNING] Transient error on attempt {attempt}/{max_retries}: {result_push.stderr.strip()}")
                print(f"[INFO] Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue

            # Non-transient error or last attempt - check if branch exists anyway
            if attempt == max_retries:
                print("[INFO] Verifying if branch exists on remote...")
                verify_remote = subprocess.run(
                    ["git", "ls-remote", "--heads", "origin", branch_name],
                    cwd=repo_path,
                    capture_output=True,
                    check=False,
                    encoding="utf-8",
                    errors="replace",
                )
                if verify_remote.returncode == 0 and verify_remote.stdout.strip():
                    print("[OK] Branch exists on remote (verified via ls-remote)")
                    return True

            print(f"[ERROR] Failed to push branch (attempt {attempt}/{max_retries}): {result_push.stderr}", file=sys.stderr)

        return False

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to create/push branch: {e}", file=sys.stderr)
        return False


def update_root_branch(repo_path: Path, root_branch: str) -> None:
    """Checkout and pull the root branch in repo_path.

    Args:
        repo_path: Path to the Git repository
        root_branch: Root branch name

    Raises:
        RuntimeError on failure
    """
    print(f"[INFO] Switching to {root_branch} branch...")
    safe_run(["git", "checkout", root_branch], cwd=repo_path, check=True, capture_output=True)
    safe_run(["git", "pull", "origin", root_branch], cwd=repo_path, check=True, capture_output=True)
    print(f"[OK] Updated {root_branch} branch")


def delete_local_branch(repo_path: Path, branch: str) -> bool:
    """Attempt to delete a local branch.

    Args:
        repo_path: Path to the Git repository
        branch: Branch name to delete

    Returns:
        True on success, False otherwise
    """
    print(f"[INFO] Deleting local branch {branch}...")
    try:
        safe_run(["git", "branch", "-d", branch], cwd=repo_path, check=True, capture_output=True)
        print(f"[OK] Deleted local branch {branch}")
        return True
    except RuntimeError:
        return False


def delete_remote_branch(repo_path: Path, branch: str) -> bool:
    """Attempt to delete a remote branch.

    Args:
        repo_path: Path to the Git repository
        branch: Branch name to delete

    Returns:
        True on success, False otherwise
    """
    print(f"[INFO] Deleting remote branch {branch}...")
    try:
        safe_run(["git", "push", "origin", "--delete", branch], cwd=repo_path, check=True, capture_output=True)
        print(f"[OK] Deleted remote branch {branch}")
        return True
    except RuntimeError:
        return False


def count_modified_files(repo_path: Path) -> int:
    """Count modified files in the repository.

    Args:
        repo_path: Path to the Git repository

    Returns:
        Number of modified files
    """
    try:
        result = safe_run(["git", "status", "--porcelain"], cwd=repo_path, capture_output=True, text=True)
        output = result.stdout or ""
        changes = output.strip().split("\n") if output.strip() else []
        return len([c for c in changes if c])
    except RuntimeError:
        return 0


def push_branch_changes(repo_path: Path, branch_name: str) -> None:
    """Push the current branch to remote. Raises SystemExit on failure.

    Args:
        repo_path: Path to the Git repository
        branch_name: Expected branch name (for warning if mismatch)
    """
    current_branch = get_current_branch(repo_path)
    if not current_branch or branch_name not in current_branch:
        print(f"[WARNING] Current branch '{current_branch}' doesn't match expected '{branch_name}'")
    push_latest_changes(repo_path, branch_name, current_branch)


def create_pull_request(repo_config: dict[str, Any], repo_path: Path, jira_ticket: str, summary: str) -> Optional[Any]:  # type: ignore[type-arg]
    """Create a pull request on GitHub. Returns PR object or None on failure."""
    print("[INFO] Creating pull request...")
    try:

        token = get_github_token()  # type: ignore[no-untyped-call]
        gh = Github(token)  # type: ignore[var-annotated,no-untyped-call]
        owner, repo_name = get_repo_from_url(repo_config["url"])  # type: ignore[arg-type]
        repo = gh.get_repo(f"{owner}/{repo_name}")  # type: ignore[var-annotated,no-untyped-call]
        commits = get_commits_since_branch(repo_path, repo_config.get("root_branch", "develop") or "develop")  # type: ignore[arg-type]
        pr_title = f"{jira_ticket}: {summary}"
        jira_server = repo_config.get("jira_server", DEFAULT_JIRA_SERVER) or DEFAULT_JIRA_SERVER
        pr_body = build_pr_body(jira_ticket, jira_server, summary, commits)  # type: ignore[arg-type]
        base_branch = repo_config.get("root_branch", "develop") or "develop"
        current_branch = get_current_branch(repo_path) or "develop"
        pr = repo.create_pull(
            title=pr_title,
            body=pr_body,
            head=current_branch,
            base=base_branch,
        )  # type: ignore[var-annotated,no-untyped-call]
        print(f"[OK] Pull request created: {pr.html_url}")  # type: ignore[no-untyped-call]
        print(f"[OK] PR #{pr.number}: {pr_title}")  # type: ignore[no-untyped-call]
        return pr  # type: ignore[return-value]
    except (OSError, subprocess.SubprocessError) as e:
        print(f"[ERROR] Failed to create pull request: {e}", file=sys.stderr)
        print("[INFO] You can create the PR manually on GitHub", file=sys.stderr)
        return None
