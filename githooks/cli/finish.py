"""
Finish command handler for git-go
"""

import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from githooks.core.constants import DEFAULT_JIRA_SERVER
from githooks.core.github_utils import create_branch_name, create_pull_request, get_current_branch  # type: ignore[attr-defined]
from githooks.core.jira_helpers import connect_to_jira, fetch_jira_issue, transition_to_review_state  # type: ignore[attr-defined]
from githooks.core.repo_helpers import load_repo_config, verify_repo_exists
from githooks.core.utils import GitGoError, ensure_dependencies, push_latest_changes

# Configure logging
LOG_LEVEL = os.environ.get("GIT_GO_LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO), format="[%(levelname)s] %(message)s")
logger = logging.getLogger("git-go")


def main(args: Any) -> None:
    """Create a pull request for a JIRA ticket: push branch, transition JIRA, and create PR.

    The main function is now a thin orchestrator that reads like sequential steps
    by delegating work to focused helper functions.
    """
    try:
        ensure_dependencies()
        repo_alias = args.repo_alias
        jira_ticket = args.jira_ticket.upper()
        logger.info("📝 Creating pull request for %s in %s repository", jira_ticket, repo_alias)

        repo_config = load_repo_config(repo_alias)
        jira_server = repo_config.get("jira_server", DEFAULT_JIRA_SERVER)
        jira = connect_to_jira(jira_server)  # type: ignore[assignment]
        summary = fetch_jira_issue(jira, jira_ticket)  # type: ignore[arg-type]

        branch_name = create_branch_name(jira_ticket, summary, repo_config.get("branch_prefix", ""), repo_config.get("root_branch", "develop"))
        repo_path = locate_repo(repo_config, branch_name)

        push_branch_changes(repo_path, branch_name)
        transition_to_review_state(jira, jira_ticket, branch_name)  # type: ignore[arg-type]

        pr = create_pull_request(repo_config, repo_path, jira_ticket, summary)
        if pr:
            logger.info("✅ Success! Pull request created for %s", jira_ticket)
            logger.info("   PR URL: %s", pr.html_url)  # type: ignore[attr-defined]
            logger.info("   JIRA: %s/browse/%s", repo_config.get("jira_server", DEFAULT_JIRA_SERVER), jira_ticket)
    except GitGoError as e:
        logger.error("%s", e)
        sys.exit(1)


def locate_repo(repo_config: Dict[str, Any], branch_name: str) -> Path:
    """Locate the repository directory for the given branch name.

    Args:
        repo_config (Dict[str, Any]): The repository configuration.
        branch_name (str): The branch name.
    Returns:
        Path: The path to the repository directory.
    """
    clone_to = str(repo_config["clone_to"])
    dir_name = branch_name.split("/")[-1] if "/" in branch_name else branch_name
    repo_path = Path(clone_to) / dir_name
    verify_repo_exists(repo_path, "branch work")
    return repo_path


def push_branch_changes(repo_path: Path, branch_name: str) -> None:
    """Push the current branch to remote.

    Args:
        repo_path (Path): The path to the repository.
        branch_name (str): The branch name to push.
    Raises:
        SystemExit: If the current branch cannot be determined.
    """
    current_branch: Optional[str] = get_current_branch(repo_path)
    # Ensure current_branch is a string, not None, for type safety
    push_latest_changes(repo_path, branch_name, current_branch if current_branch is not None else "")
