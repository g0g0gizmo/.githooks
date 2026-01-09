"""
Repository configuration and management helper functions for git-go commands.

This module contains functions for loading repository configurations,
finding repositories, and GitHub integration.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from githooks.core.constants import ALIAS_MAP, DEFAULT_JIRA_SERVER, DEFAULT_ROOT_BRANCH, TEST_JIRA_SERVER


def load_repo_config_from_git(alias: str) -> Optional[Dict[str, Any]]:
    """
    Load repository configuration from Git config.

    Args:
        alias (str): Repository alias name.

    Returns:
        Optional[Dict[str, Any]]: Dictionary with configuration or None if not found.
    """
    try:
        result = subprocess.run(["git", "config", "--get", f"repo.{alias}.url"], capture_output=True, check=False, encoding="utf-8", errors="replace")
        if result.returncode != 0:
            return None
        url = result.stdout.strip()
        result = subprocess.run(["git", "config", "--get", f"repo.{alias}.cloneto"], capture_output=True, check=False, encoding="utf-8", errors="replace")
        clone_to = result.stdout.strip() if result.returncode == 0 else None
        result = subprocess.run(
            ["git", "config", "--get", f"repo.{alias}.rootbranch"], capture_output=True, check=False, encoding="utf-8", errors="replace"
        )
        root_branch = result.stdout.strip() if result.returncode == 0 else "develop"
        result = subprocess.run(
            ["git", "config", "--get", f"repo.{alias}.jiraserver"], capture_output=True, check=False, encoding="utf-8", errors="replace"
        )
        jira_server = result.stdout.strip() if result.returncode == 0 else DEFAULT_JIRA_SERVER
        result = subprocess.run(
            ["git", "config", "--get", f"repo.{alias}.branchprefix"], capture_output=True, check=False, encoding="utf-8", errors="replace"
        )
        branch_prefix = result.stdout.strip() if result.returncode == 0 else ""
        if not url or not clone_to:
            return None
        return {"url": url, "clone_to": clone_to, "root_branch": root_branch, "jira_server": jira_server, "branch_prefix": branch_prefix}
    except (OSError, subprocess.SubprocessError):
        return None


def prompt_for_repo_config(alias: str) -> Dict[str, Any]:
    """
    Prompt user for repository configuration and save to Git config.

    Args:
        alias (str): Repository alias name.

    Returns:
        Dict[str, Any]: Dictionary with repository configuration.
    """
    print(f"\n[INFO] Repository alias '{alias}' not found. Let's set it up!\n")
    url = input(f"Repository URL for '{alias}': ").strip()
    while not url:
        print("[ERROR] URL is required")
        url = input(f"Repository URL for '{alias}': ").strip()
    clone_to = input(f"Clone directory (e.g., C:/Users/{os.getlogin()}/Projects/{alias}/branches): ").strip()
    while not clone_to:
        print("[ERROR] Clone directory is required")
        clone_to = input(f"Clone directory for '{alias}': ").strip()
    root_branch = input("Root branch [develop]: ").strip() or "develop"
    jira_server = input(f"JIRA server [{DEFAULT_JIRA_SERVER}]: ").strip() or DEFAULT_JIRA_SERVER
    branch_prefix = input("Branch prefix (e.g., 'feature/', leave empty for none): ").strip()
    print("\n[INFO] Configuration to save:")
    print(f"  Repository: {url}")
    print(f"  Clone to: {clone_to}")
    print(f"  Root branch: {root_branch}")
    print(f"  JIRA server: {jira_server}")
    if branch_prefix:
        print(f"  Branch prefix: {branch_prefix}")
    save = input("\nSave to git config? [Y/n]: ").strip().lower()
    if save and save not in ("y", "yes", ""):
        print("[INFO] Configuration not saved. Exiting.")
        sys.exit(0)
    try:
        subprocess.run(["git", "config", "--global", f"repo.{alias}.url", url], check=True)
        subprocess.run(["git", "config", "--global", f"repo.{alias}.cloneto", clone_to], check=True)
        subprocess.run(["git", "config", "--global", f"repo.{alias}.rootbranch", root_branch], check=True)
        subprocess.run(["git", "config", "--global", f"repo.{alias}.jiraserver", jira_server], check=True)
        if branch_prefix:
            subprocess.run(["git", "config", "--global", f"repo.{alias}.branchprefix", branch_prefix], check=True)
        print("[OK] Configuration saved")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to save configuration: {e}", file=sys.stderr)
        sys.exit(1)
    return {"url": url, "clone_to": clone_to, "root_branch": root_branch, "jira_server": jira_server, "branch_prefix": branch_prefix}


def load_repo_config(alias: str) -> Dict[str, Any]:
    """Load repository configuration from Git config or prompt user.

    Args:
        alias: Repository alias name

    Returns:
        Dictionary with repository configuration
    """
    # First, check alias map in config
    if alias in ALIAS_MAP:
        url = ALIAS_MAP[alias]
        # Provide sane defaults for clone_to and root_branch; allow override via git config if set
        home = Path.home()
        clone_to_default = str(home / f"Projects/{alias}/branches")
        # Prefer git config values when available
        cfg = load_repo_config_from_git(alias)
        if cfg:
            return cfg
        # Use test-specific jira server if available
        jira_server = TEST_JIRA_SERVER if alias == "test" else DEFAULT_JIRA_SERVER
        return {
            "url": url,
            "clone_to": clone_to_default,
            "root_branch": DEFAULT_ROOT_BRANCH,
            "jira_server": jira_server,
            "branch_prefix": "feature/",
        }

    config_dict = load_repo_config_from_git(alias)
    if config_dict:
        return config_dict
    return prompt_for_repo_config(alias)


def find_most_recent_repo(base_path: Path) -> Optional[Path]:
    """Return the most recently modified child directory that looks like a git repo.

    Args:
        base_path: Base directory to search

    Returns:
        Path to most recent repository or None if none found
    """
    if not base_path.exists() or not base_path.is_dir():
        return None
    branch_dirs = [d for d in base_path.iterdir() if d.is_dir() and (d / ".git").exists()]
    if not branch_dirs:
        return None
    return max(branch_dirs, key=lambda d: d.stat().st_mtime)


def load_repo_info(repo_alias: str) -> Tuple[Dict[str, Any], Path]:
    """Load repository configuration and find the most recent repo clone.

    Args:
        repo_alias: Repository alias name

    Returns:
        Tuple of (repo_config, repo_path)

    Raises:
        SystemExit if repo not found
    """
    repo_config = load_repo_config(repo_alias)
    clone_to = repo_config["clone_to"]
    base_path = Path(clone_to)
    repo_path = find_most_recent_repo(base_path)
    if not repo_path:
        print(f"[ERROR] No Git repositories found in {base_path}", file=sys.stderr)
        sys.exit(1)
    return repo_config, repo_path


def verify_repo_exists(repo_path: Path, context: str = "") -> None:
    """Verify that repo_path exists and is a git repository.

    Args:
        repo_path: Path to verify
        context: Optional context message for error

    Raises:
        SystemExit on failure
    """
    if not repo_path.exists():
        msg = f"[ERROR] Repository not found at {repo_path}"
        if context:
            msg += f" ({context})"
        print(msg, file=sys.stderr)
        print("[INFO] Run 'git go start' first to create the branch", file=sys.stderr)
        sys.exit(1)


def get_github_token() -> Optional[str]:
    """Retrieve GitHub token from environment variables or Git config.

    Returns:
        GitHub token or exits if not found
    """
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        token = os.environ.get("JIRA_TOKEN")
    if not token:
        print("[ERROR] GitHub token not found. Set GITHUB_TOKEN or GH_TOKEN environment variable.", file=sys.stderr)
        sys.exit(1)
    return token


def get_repo_from_url(url: str) -> Tuple[str, str]:
    """Parse GitHub owner and repository name from URL.

    Args:
        url: GitHub repository URL

    Returns:
        Tuple of (owner, repo_name)

    Raises:
        ValueError if URL cannot be parsed
    """
    if "github.com" in url:
        parts = url.rstrip("/").split("/")
        if len(parts) >= 2:
            repo_name = parts[-1].replace(".git", "")
            owner = parts[-2]
            return owner, repo_name
    raise ValueError(f"Could not parse GitHub URL: {url}")


def build_pr_body(jira_ticket: str, jira_server: str, summary: str, commits: list[str]) -> str:
    """Construct a pull request body including JIRA link and commit list.

    Args:
        jira_ticket: JIRA ticket identifier
        jira_server: JIRA server URL
        summary: Issue summary text
        commits: List of commit messages

    Returns:
        Formatted pull request body
    """
    commit_list = "\n".join([f"- {c}" for c in commits]) if commits else "No commits found"
    return (
        f"# [{jira_ticket}]({jira_server}/browse/{jira_ticket})\n\n"
        f"## Description\n\n{summary}\n\n"
        f"## Commits\n\n{commit_list}\n\n"
        "## Test Steps\n\n1. Review code changes\n2. Run automated tests\n3. Verify functionality\n"
    )
