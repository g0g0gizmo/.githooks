"""
Start command handler for git-go
"""

import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict

from githooks.core.constants import DEFAULT_JIRA_SERVER
from githooks.core.github_issues import get_issue as get_github_issue
from githooks.core.github_issues import transition_to_in_progress
from githooks.core.github_utils import clone_or_update_repo, create_and_push_branch, create_branch_name
from githooks.core.jira_helpers import connect_to_jira, fetch_jira_issue, transition_jira_ticket  # type: ignore[attr-defined]
from githooks.core.repo_helpers import get_repo_from_url, load_repo_config
from githooks.core.utils import GitGoError, ensure_dependencies

# Configure logging
LOG_LEVEL = os.environ.get("GIT_GO_LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO), format="[%(levelname)s] %(message)s")
logger = logging.getLogger("git-go")


def main(args: Any) -> None:
    """Start work on an issue: create branch, clone repo, and transition issue.

    Supports both JIRA tickets (PROJ-123) and GitHub Issues (#123).
    The issue type is detected from the input format.

    The main function is now a thin orchestrator that reads like sequential steps
    by delegating work to focused helper functions.
    """
    try:
        ensure_dependencies()
        repo_alias = args.repo_alias
        issue_ref = args.jira_ticket  # Can be JIRA ticket or GitHub issue number

        # Detect if this is a GitHub issue (starts with # or is just a number)
        is_github_issue = issue_ref.startswith("#") or issue_ref.isdigit()

        if is_github_issue:
            # GitHub Issue workflow
            issue_number = int(issue_ref.lstrip("#"))
            logger.info("🚀 Starting work on GitHub issue #%d in %s repository", issue_number, repo_alias)

            repo_config = load_repo_config_for_alias(repo_alias)
            owner, repo_name = get_repo_from_url(repo_config["url"])

            # Fetch issue details from GitHub
            issue_data = get_github_issue(owner, repo_name, issue_number)
            if not issue_data:
                raise GitGoError(f"Failed to fetch GitHub issue #{issue_number}")

            summary = issue_data["title"]
            logger.info("Issue title: %s", summary)

            # Create branch name: issue-123-description or 123-description
            branch_prefix = repo_config.get("branch_prefix", "")
            if branch_prefix:
                branch_name = f"{branch_prefix}issue-{issue_number}-{format_for_branch(summary)}"
            else:
                branch_name = f"issue-{issue_number}-{format_for_branch(summary)}"
            logger.info("Branch name: %s", branch_name)

            repo_path = clone_and_push_branch(repo_config, branch_name)

            # Transition GitHub issue to 'in progress'
            if transition_to_in_progress(owner, repo_name, issue_number, branch_name):
                logger.info("✅ Success! You're ready to work on #%d", issue_number)
            else:
                logger.warning("⚠️  Branch created but failed to transition issue")

            logger.info("   Repository: %s", repo_path)
            logger.info("   Branch: %s", branch_name)
            logger.info("   GitHub Issue: https://github.com/%s/%s/issues/%d", owner, repo_name, issue_number)

        else:
            # JIRA workflow (existing)
            jira_ticket = issue_ref.upper()
            logger.info("🚀 Starting work on JIRA %s in %s repository", jira_ticket, repo_alias)

            repo_config = load_repo_config_for_alias(repo_alias)
            jira_server = repo_config.get("jira_server", DEFAULT_JIRA_SERVER)
            jira = connect_to_jira(jira_server)
            summary = fetch_jira_issue(jira, jira_ticket)

            branch_name = create_branch_name(jira_ticket, summary, repo_config.get("branch_prefix", ""), repo_config.get("root_branch", "develop"))
            logger.info("Branch name: %s", branch_name)

            repo_path = clone_and_push_branch(repo_config, branch_name)

            transition_jira_ticket(jira, jira_ticket, branch_name)

            logger.info("✅ Success! You're ready to work on %s", jira_ticket)
            logger.info("   Repository: %s", repo_path)
            logger.info("   Branch: %s", branch_name)
            logger.info("   JIRA: %s/browse/%s", repo_config.get("jira_server", DEFAULT_JIRA_SERVER), jira_ticket)
    except GitGoError as e:
        logger.error("%s", e)
        sys.exit(1)


def load_repo_config_for_alias(repo_alias: str):
    """Load repository configuration for the given alias.

    Args:
        repo_alias (str): The alias of the repository.
    Returns:
        dict: The repository configuration dictionary.
    """
    return load_repo_config(repo_alias)


def format_for_branch(text: str, max_length: int = 50) -> str:
    """Format text for use in branch name (lowercase, hyphens, no special chars).

    Args:
        text: Text to format (e.g., issue title)
        max_length: Maximum length of formatted text

    Returns:
        Formatted text suitable for branch name
    """
    # Convert to lowercase and replace spaces/underscores with hyphens
    formatted = text.lower().replace(" ", "-").replace("_", "-")
    # Remove special characters except hyphens
    formatted = "".join(c for c in formatted if c.isalnum() or c == "-")
    # Remove consecutive hyphens
    while "--" in formatted:
        formatted = formatted.replace("--", "-")
    # Trim to max length
    formatted = formatted[:max_length].strip("-")
    return formatted


def clone_and_push_branch(repo_config: Dict[str, str], branch_name: str) -> Path:
    """Clone or update repo and create/push branch.

    Args:
        repo_config (Dict[str, str]): The repository configuration.
        branch_name (str): The branch name to create and push.
    Returns:
        Path: The path to the local repository.
    Raises:
        SystemExit: If branch creation or push fails.
    """
    url = repo_config["url"]
    clone_to = repo_config["clone_to"]
    root_branch = repo_config.get("root_branch", "develop")
    repo_path = clone_or_update_repo(url, clone_to, root_branch, branch_name)
    if not create_and_push_branch(repo_path, branch_name, root_branch):
        sys.exit(1)
    return repo_path
