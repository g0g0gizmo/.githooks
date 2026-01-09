"""
Publish command handler for git-go
"""

import logging
import os
import sys
from typing import Any

from githooks.core.constants import DEFAULT_JIRA_SERVER
from githooks.core.github_utils import delete_local_branch, delete_remote_branch, get_current_branch, get_ticket_from_branch, update_root_branch
from githooks.core.jira_helpers import get_jira_client, transition_to_done_state  # type: ignore[attr-defined]
from githooks.core.repo_helpers import load_repo_info
from githooks.core.utils import GitGoError, ensure_dependencies

# Configure logging
LOG_LEVEL = os.environ.get("GIT_GO_LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO), format="[%(levelname)s] %(message)s")
logger = logging.getLogger("git-go")


def main(args: Any) -> None:
    """Publish latest work for a repo alias: transition JIRA, update root branch and cleanup.

    The `main` function is now a thin orchestrator that reads like sequential
    steps by delegating work to focused helper functions.

    Args:
        args (Any): The command-line arguments namespace.
    """
    try:
        ensure_dependencies()
        repo_alias = args.repo_alias
        logger.info("🚢 Publishing changes for %s repository", repo_alias)

        repo_config, repo_path = load_repo_info(repo_alias)
        logger.info("Using repository: %s", repo_path)

        current_branch = get_current_branch(repo_path)
        if not current_branch:
            logger.error("Failed to get current branch")
            sys.exit(1)

        jira_ticket = get_ticket_from_branch(current_branch)
        logger.info("JIRA Ticket: %s", jira_ticket)

        jira_server = repo_config.get("jira_server", DEFAULT_JIRA_SERVER)
        jira = get_jira_client(jira_server)
        if jira:
            transition_to_done_state(jira, jira_ticket)

        root_branch = repo_config.get("root_branch", "develop")
        try:
            update_root_branch(repo_path, root_branch)
        except RuntimeError as e:
            logger.error("Failed to update %s: %s", root_branch, e)

        deleted_local = delete_local_branch(repo_path, current_branch)
        if not deleted_local:
            logger.warning("Could not delete local branch (may have unmerged changes)")

        deleted_remote = delete_remote_branch(repo_path, current_branch)
        if not deleted_remote:
            logger.warning("Could not delete remote branch")

        logger.info("✅ Success! Changes published for %s", jira_ticket)
        logger.info("   JIRA: %s/browse/%s", jira_server, jira_ticket)
        logger.info("   Branch cleaned up: %s", current_branch)
    except GitGoError as e:
        logger.error("%s", e)
        sys.exit(1)
