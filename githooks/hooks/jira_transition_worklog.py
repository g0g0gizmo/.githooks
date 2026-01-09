"""
Python module for Jira transition worklog logic, extracted from the post-checkout hook for testability.
"""

import subprocess
import sys
from typing import Optional, Tuple

import keyring  # imported for test monkeypatching
import typer  # imported for test compatibility
from jira import JIRA  # imported for test compatibility

from githooks.core.constants import BRANCH_REGEX as _BRANCH_REGEX
from githooks.core.constants import DEFAULT_JIRA_SERVER
from githooks.core.constants import SERVICE_NAME as _SERVICE_NAME
from githooks.core.constants import WORKLOG_TRANSITION_TIME
from githooks.core.jira_client import get_jira_client, parse_ticket_from_branch

# Re-export constants for backward compatibility with tests
BRANCH_REGEX = _BRANCH_REGEX
SERVICE_NAME = _SERVICE_NAME
DEFAULT_SERVER = DEFAULT_JIRA_SERVER

# Hook-specific default
DEFAULT_TIME_SPENT = WORKLOG_TRANSITION_TIME

# Required dependencies for JIRA integration
REQUIRED_DEPENDENCIES = {
    "jira": "jira",
    "keyring": "keyring",
    "typer": "typer",
}


def ensure_dependencies():
    """Ensure required dependencies are installed.

    If dependencies are missing, attempts to install them via pip.
    Exits with code 1 if installation fails.
    """
    import importlib.util

    missing = []
    for module_name in REQUIRED_DEPENDENCIES.keys():
        if importlib.util.find_spec(module_name) is None:
            missing.append(module_name)

    if not missing:
        return

    print(f"[INFO] Installing missing dependencies: {', '.join(missing)}", file=sys.stderr)
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--user"] + missing, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to install dependencies: {e}", file=sys.stderr)
        sys.exit(1)


def transition_and_log_work(jira, ticket: str, branch_name: str, time_spent: str = DEFAULT_TIME_SPENT) -> Tuple[bool, Optional[str]]:
    """Transition ticket to 'In Progress' and log work.

    Args:
        jira: Authenticated JIRA client instance
        ticket: JIRA ticket identifier
        branch_name: Git branch name
        time_spent: Time to log (default: WORKLOG_TRANSITION_TIME)

    Returns:
        Tuple of (success: bool, error_message: Optional[str])
    """
    try:
        comment = f"Started work on {branch_name}"
        issue = jira.issue(ticket)
        jira.add_worklog(issue, timeSpent=time_spent, comment=comment)
        transitions = jira.transitions(issue)
        open_transition = next((t for t in transitions if "open" in t["name"].lower()), None)
        if open_transition:
            jira.transition_issue(issue, open_transition["id"])
            transitions = jira.transitions(issue)
        in_progress = next((t for t in transitions if "progress" in t["name"].lower()), None)
        if in_progress:
            jira.transition_issue(issue, in_progress["id"])
        return True, None
    except Exception as exc:
        return False, f"Failed to transition/log work: {exc}"


# Expose for testing
__all__ = [
    "parse_ticket_from_branch",
    "get_jira_client",
    "transition_and_log_work",
    "ensure_dependencies",
    "BRANCH_REGEX",
    "SERVICE_NAME",
    "DEFAULT_SERVER",
    "DEFAULT_TIME_SPENT",
    "REQUIRED_DEPENDENCIES",
]
