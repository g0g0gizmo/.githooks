"""
Start command handler for git-go
"""

import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict

from githooks.core.constants import DEFAULT_JIRA_SERVER
from githooks.core.github_utils import clone_or_update_repo, create_and_push_branch, create_branch_name
from githooks.core.jira_helpers import connect_to_jira, fetch_jira_issue, transition_jira_ticket  # type: ignore[attr-defined]
from githooks.core.repo_helpers import load_repo_config
from githooks.core.utils import GitGoError, ensure_dependencies

# Configure logging
LOG_LEVEL = os.environ.get("GIT_GO_LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO), format="[%(levelname)s] %(message)s")
logger = logging.getLogger("git-go")


def main(args: Any) -> None:
    """Start work on a JIRA ticket: create branch, clone repo, and transition JIRA.

    The main function is now a thin orchestrator that reads like sequential steps
    by delegating work to focused helper functions.
    """
    try:
        ensure_dependencies()
        repo_alias = args.repo_alias
        jira_ticket = args.jira_ticket.upper()
        logger.info("🚀 Starting work on %s in %s repository", jira_ticket, repo_alias)

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
