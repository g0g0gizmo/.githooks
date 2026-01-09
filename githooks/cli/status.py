"""
Status command handler for git-go
"""

import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

from githooks.core.constants import DEFAULT_JIRA_SERVER
from githooks.core.github_utils import count_modified_files, extract_ticket_from_branch, get_commits_since_branch, get_current_branch
from githooks.core.jira_helpers import get_jira_client
from githooks.core.repo_helpers import load_repo_config, load_repo_info
from githooks.core.utils import GitGoError, ensure_dependencies

# Configure logging
LOG_LEVEL = os.environ.get("GIT_GO_LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO), format="[%(levelname)s] %(message)s")
logger = logging.getLogger("git-go")


def main(args: Any) -> None:
    """Show workflow status for most recent branch repo under the alias clone dir.

    The main function is now a thin orchestrator that reads like sequential
    steps by delegating work to focused helper functions.
    """
    try:
        ensure_dependencies()
        repo_alias = args.repo_alias
        logger.info("📊 Workflow Status for %s", repo_alias)

        repo_config = load_repo_config(repo_alias)
        repo_path = find_latest_repo(repo_alias)
        current_branch = get_and_verify_branch(repo_path)
        modified_count = count_modified_files(repo_path)
        jira_ticket = extract_ticket_from_branch(current_branch)

        display_git_status(current_branch, modified_count, repo_path)

        if jira_ticket:
            display_jira_status(repo_config, jira_ticket)

        commits = get_commits_since_branch(repo_path, repo_config.get("root_branch", "develop"))
        display_commits(commits)
        display_next_steps(modified_count, commits)
    except GitGoError as e:
        logger.error("%s", e)
        sys.exit(1)


def find_latest_repo(repo_alias: str) -> Path:
    """Find the most recent repo clone in the configured clone directory.

    Args:
        repo_alias (str): The repository alias.
    Returns:
        Path: The path to the most recent repository clone.
    """
    _, repo_path = load_repo_info(repo_alias)
    return repo_path


def get_and_verify_branch(repo_path: Path) -> str:
    """Get the current branch name.

    Args:
        repo_path (Path): The path to the repository.
    Returns:
        str: The current branch name.
    Raises:
        SystemExit: If the current branch cannot be determined.
    """
    current_branch = get_current_branch(repo_path)
    if not current_branch:
        logger.error("Failed to get current branch")
        sys.exit(1)
    return current_branch


def display_git_status(current_branch: str, modified_count: int, repo_path: Path) -> None:
    """Display git status information.

    Args:
        current_branch (str): The current branch name.
        modified_count (int): Number of modified files.
        repo_path (Path): The path to the repository.
    """
    logger.info("┌─ Git Status ─────────────────────────────────┐")
    logger.info("│ Branch:      %-30s │", current_branch[:30])
    logger.info("│ Changes:     %s files modified%s │", modified_count, " " * (30 - len(str(modified_count)) - 16))
    logger.info("│ Repository:  %-30s │", str(repo_path)[-30:])
    logger.info("└───────────────────────────────────────────────┘\n")


def display_jira_status(repo_config: Dict[str, Any], jira_ticket: str) -> None:
    """Display JIRA issue status.

    Args:
        repo_config (Dict[str, Any]): The repository configuration.
        jira_ticket (str): The JIRA ticket identifier.
    """
    jira_server = repo_config.get("jira_server", DEFAULT_JIRA_SERVER)
    jira = get_jira_client(jira_server)
    if not jira:
        return

    try:
        issue = jira.issue(jira_ticket)
        time_spent = getattr(issue.fields.timetracking, "timeSpent", "Not tracked")
        time_estimate = getattr(issue.fields.timetracking, "originalEstimate", "No estimate")
        logger.info("┌─ JIRA Status ────────────────────────────────┐")
        logger.info("│ Issue:       %-30s │", jira_ticket)
        logger.info("│ Title:       %-30s │", issue.fields.summary[:30])
        logger.info("│ Status:      %-30s │", str(issue.fields.status)[:30])
        logger.info("│ Time Logged: %s/%s%s │", time_spent, time_estimate, " " * (30 - len(str(time_spent)) - len(str(time_estimate)) - 1))
        logger.info("│ Assignee:    %-30s │", str(issue.fields.assignee)[:30])
        logger.info("└───────────────────────────────────────────────┘\n")
    except (OSError, subprocess.SubprocessError) as e:
        logger.warning("Could not fetch JIRA status: %s", e)


def display_commits(commits: list[str]) -> None:
    """Display commits since the root branch.

    Args:
        commits (list[str]): List of commit messages since the root branch.
    """
    if not commits:
        return

    logger.info("┌─ Commits ────────────────────────────────────┐")
    for commit in commits[:5]:
        commit_short = commit[:45] if len(commit) > 45 else commit
        logger.info("│ • %-44s │", commit_short)
    if len(commits) > 5:
        logger.info("│ ... and %s more%s │", len(commits) - 5, " " * (35 - len(str(len(commits) - 5))))
    logger.info("└───────────────────────────────────────────────┘\n")


def display_next_steps(modified_count: int, commits: list[str]) -> None:
    """Display recommended next steps based on current status.

    Args:
        modified_count (int): Number of modified files.
        commits (list[str]): List of commit messages since the root branch.
    """
    if modified_count > 0:
        logger.info("⏭️  Next: Commit changes and push")
    elif commits:
        logger.info("⏭️  Next: Run 'git go finish' to create PR")
    else:
        logger.info("⏭️  Next: Make changes and commit")
    logger.info("")
