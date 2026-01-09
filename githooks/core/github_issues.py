"""
GitHub Issues API client and integration utilities.

This module provides GitHub Issues integration for git-go workflows:
- Fetching issue details (title, description, labels, state)
- Adding comments to issues
- Updating issue labels and state transitions
- Authentication via GitHub token (environment variable or keyring)

This is parallel to jira_client.py and provides similar functionality for GitHub Issues.

Architecture:
    CLI Commands → issue_tracker (detection) → github_issues (this module) OR jira_client

Authentication:
    - GITHUB_TOKEN environment variable
    - GITHUB_USERNAME + keyring storage
    - Interactive prompt if neither is available
"""

import getpass
import os
import sys
from typing import Any, Dict, Optional

import keyring
from github import Github, GithubException  # type: ignore[import]

from githooks.core.constants import SERVICE_NAME


def get_github_credentials() -> str:
    """Retrieve GitHub token from environment, keyring, or user input.

    Returns:
        GitHub personal access token
    """
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

    if not token:
        token = keyring.get_password(f"{SERVICE_NAME}.github.token", "token")  # type: ignore[union-attr]

    if not token:
        print("[INFO] GitHub token not found in environment or keyring")
        token = getpass.getpass("Enter your GitHub personal access token: ")
        # Ask if user wants to save token
        save = input("Save token to system keyring? (y/n): ").strip().lower()
        if save == "y":
            keyring.set_password(f"{SERVICE_NAME}.github.token", "token", token)  # type: ignore[union-attr]
            print("[OK] Token saved to keyring")

    return token


def get_github_client() -> Optional[Github]:
    """Create and return an authenticated GitHub client instance.

    Returns:
        Authenticated Github client instance, or None if authentication fails
    """
    try:
        token = get_github_credentials()
        if not token:
            print("[ERROR] No GitHub token provided", file=sys.stderr)
            return None

        client = Github(token)
        # Test authentication by getting the user
        client.get_user().login  # type: ignore[no-untyped-call]
        return client
    except GithubException as e:
        print(f"[ERROR] Failed to authenticate with GitHub: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[ERROR] Failed to create GitHub client: {e}", file=sys.stderr)
        return None


def get_issue(repo_owner: str, repo_name: str, issue_number: int) -> Optional[Dict[str, Any]]:
    """Fetch GitHub issue details.

    Args:
        repo_owner: Repository owner (e.g., 'octocat')
        repo_name: Repository name (e.g., 'Hello-World')
        issue_number: Issue number

    Returns:
        Dictionary with issue details (title, body, state, labels) or None on failure
    """
    client = get_github_client()
    if not client:
        return None

    try:
        repo = client.get_repo(f"{repo_owner}/{repo_name}")
        issue = repo.get_issue(issue_number)

        return {
            "number": issue.number,
            "title": issue.title,
            "body": issue.body or "",
            "state": issue.state,
            "labels": [label.name for label in issue.labels],
            "url": issue.html_url,
        }
    except GithubException as e:
        print(f"[ERROR] Failed to fetch issue #{issue_number}: {e}", file=sys.stderr)
        return None


def add_comment(repo_owner: str, repo_name: str, issue_number: int, comment: str) -> bool:
    """Add a comment to a GitHub issue.

    Args:
        repo_owner: Repository owner
        repo_name: Repository name
        issue_number: Issue number
        comment: Comment text

    Returns:
        True if successful, False otherwise
    """
    client = get_github_client()
    if not client:
        return False

    try:
        repo = client.get_repo(f"{repo_owner}/{repo_name}")
        issue = repo.get_issue(issue_number)
        issue.create_comment(comment)  # type: ignore[no-untyped-call]
        print(f"[OK] Added comment to issue #{issue_number}")
        return True
    except GithubException as e:
        print(f"[ERROR] Failed to add comment to issue #{issue_number}: {e}", file=sys.stderr)
        return False


def update_issue_state(repo_owner: str, repo_name: str, issue_number: int, state: str) -> bool:
    """Update GitHub issue state (open/closed).

    Args:
        repo_owner: Repository owner
        repo_name: Repository name
        issue_number: Issue number
        state: New state ('open' or 'closed')

    Returns:
        True if successful, False otherwise
    """
    client = get_github_client()
    if not client:
        return False

    if state not in ("open", "closed"):
        print(f"[ERROR] Invalid state '{state}'. Must be 'open' or 'closed'", file=sys.stderr)
        return False

    try:
        repo = client.get_repo(f"{repo_owner}/{repo_name}")
        issue = repo.get_issue(issue_number)
        issue.edit(state=state)  # type: ignore[no-untyped-call]
        print(f"[OK] Updated issue #{issue_number} state to '{state}'")
        return True
    except GithubException as e:
        print(f"[ERROR] Failed to update issue #{issue_number}: {e}", file=sys.stderr)
        return False


def add_label(repo_owner: str, repo_name: str, issue_number: int, label: str) -> bool:
    """Add a label to a GitHub issue.

    Args:
        repo_owner: Repository owner
        repo_name: Repository name
        issue_number: Issue number
        label: Label name to add

    Returns:
        True if successful, False otherwise
    """
    client = get_github_client()
    if not client:
        return False

    try:
        repo = client.get_repo(f"{repo_owner}/{repo_name}")
        issue = repo.get_issue(issue_number)
        issue.add_to_labels(label)  # type: ignore[no-untyped-call]
        print(f"[OK] Added label '{label}' to issue #{issue_number}")
        return True
    except GithubException as e:
        print(f"[ERROR] Failed to add label to issue #{issue_number}: {e}", file=sys.stderr)
        return False


def transition_to_in_progress(repo_owner: str, repo_name: str, issue_number: int, branch_name: str) -> bool:
    """Transition GitHub issue to 'in progress' by adding label and comment.

    Args:
        repo_owner: Repository owner
        repo_name: Repository name
        issue_number: Issue number
        branch_name: Git branch name

    Returns:
        True if successful, False otherwise
    """
    comment_text = f"🚀 Work started on branch `{branch_name}`"

    # Add 'in progress' label
    if not add_label(repo_owner, repo_name, issue_number, "in progress"):
        print("[WARNING] Failed to add 'in progress' label", file=sys.stderr)

    # Add comment
    if not add_comment(repo_owner, repo_name, issue_number, comment_text):
        return False

    print(f"[OK] Transitioned issue #{issue_number} to 'in progress'")
    return True


def transition_to_review(repo_owner: str, repo_name: str, issue_number: int, branch_name: str) -> bool:
    """Transition GitHub issue to 'in review' by adding label and comment.

    Args:
        repo_owner: Repository owner
        repo_name: Repository name
        issue_number: Issue number
        branch_name: Git branch name

    Returns:
        True if successful, False otherwise
    """
    comment_text = f"🔍 Code pushed for review from branch `{branch_name}`"

    # Remove 'in progress' label, add 'in review' label
    client = get_github_client()
    if client:
        try:
            repo = client.get_repo(f"{repo_owner}/{repo_name}")
            issue = repo.get_issue(issue_number)
            # Remove 'in progress' if it exists
            current_labels = [label.name for label in issue.labels]
            if "in progress" in current_labels:
                issue.remove_from_labels("in progress")  # type: ignore[no-untyped-call]
        except GithubException:
            pass  # Non-fatal if label removal fails

    # Add 'in review' label
    if not add_label(repo_owner, repo_name, issue_number, "in review"):
        print("[WARNING] Failed to add 'in review' label", file=sys.stderr)

    # Add comment
    if not add_comment(repo_owner, repo_name, issue_number, comment_text):
        return False

    print(f"[OK] Transitioned issue #{issue_number} to 'in review'")
    return True
