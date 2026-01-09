"""
Python module for Jira add-push worklog logic, extracted from the pre-push hook for testability.
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
from githooks.core.constants import WORKLOG_PUSH_TIME
from githooks.core.jira_client import get_jira_client, parse_ticket_from_branch

# Re-export constants for backward compatibility with tests
BRANCH_REGEX = _BRANCH_REGEX
SERVICE_NAME = _SERVICE_NAME
DEFAULT_SERVER = DEFAULT_JIRA_SERVER

# Hook-specific default
DEFAULT_TIME_SPENT = WORKLOG_PUSH_TIME

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


def get_current_branch() -> Optional[str]:
    """Get the current git branch name."""
    try:
        result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, check=True, encoding="utf-8", errors="replace")
        return result.stdout.strip()
    except Exception:
        return None


def transition_to_review(jira, ticket: str, branch_name: str, time_spent: str = DEFAULT_TIME_SPENT) -> Tuple[bool, Optional[str]]:
    """Transition ticket to 'Under Review' and log work.

    Args:
        jira: Authenticated JIRA client instance
        ticket: JIRA ticket identifier
        branch_name: Git branch name
        time_spent: Time to log (default: WORKLOG_PUSH_TIME)

    Returns:
        Tuple of (success: bool, error_message: Optional[str])
    """
    try:
        comment = f"Pushed code from {branch_name} for review"
        issue = jira.issue(ticket)
        jira.add_worklog(issue, timeSpent=time_spent, comment=comment)
        transitions = jira.transitions(issue)
        under_review = next((t for t in transitions if "review" in t["name"].lower()), None)
        if under_review:
            jira.transition_issue(issue, under_review["id"])
        else:
            for transition in transitions:
                if any(keyword in transition["name"].lower() for keyword in ["code review", "peer review", "reviewing"]):
                    jira.transition_issue(issue, transition["id"])
                    break
        return True, None
    except Exception as exc:
        return False, f"Failed to transition/log work: {exc}"


def main():
    """Main entry point for pre-push hook."""
    branch = get_current_branch()
    if not branch:
        print("[ERROR] Failed to get current branch", file=sys.stderr)
        sys.exit(0)
    ticket = parse_ticket_from_branch(branch)
    if not ticket:
        sys.exit(0)
    jira_client = get_jira_client(DEFAULT_JIRA_SERVER)
    if not jira_client:
        print("[ERROR] Failed to create Jira client", file=sys.stderr)
        sys.exit(0)
    success, error = transition_to_review(jira_client, ticket, branch)
    if success:
        print(f"[OK] {ticket}: Transitioned to 'Under Review' and logged {DEFAULT_TIME_SPENT} work")
        sys.exit(0)
    else:
        print(f"[WARNING] {ticket}: {error}", file=sys.stderr)
        sys.exit(0)


# Expose for testing
__all__ = [
    "parse_ticket_from_branch",
    "get_current_branch",
    "get_jira_client",
    "transition_to_review",
    "ensure_dependencies",
    "main",
    "BRANCH_REGEX",
    "SERVICE_NAME",
    "DEFAULT_SERVER",
    "DEFAULT_TIME_SPENT",
    "REQUIRED_DEPENDENCIES",
]

if __name__ == "__main__":
    main()
