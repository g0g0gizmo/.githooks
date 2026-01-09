"""
High-level JIRA workflow operations for git-go commands.

This module provides business logic for JIRA integration in git-go workflows:
- Connecting to JIRA with error handling
- Fetching issue details and summaries
- Transitioning tickets through workflow states (In Progress, In Review, Done)
- Adding comments to track git operations

This is the business logic layer that sits above jira_client. It knows about
git-go workflows and orchestrates JIRA operations for CLI commands like
start, finish, and publish.

Architecture:
    CLI Commands (start.py, finish.py, publish.py) → jira_helpers (this module) → jira_client

Note: Authentication and client creation are handled by githooks.core.jira_client,
not this module. Import get_jira_client() from there when needed.
"""

import subprocess
import sys
from typing import Any

from githooks.core.jira_client import get_jira_client


def connect_to_jira(jira_server: str) -> Any:
    """Connect to JIRA server. Raises SystemExit on failure.

    Args:
        jira_server: JIRA server URL

    Returns:
        Connected JIRA client instance
    """
    print("[INFO] Connecting to JIRA...")
    jira = get_jira_client(jira_server)
    if not jira:
        print("[ERROR] Failed to connect to JIRA, aborting", file=sys.stderr)
        sys.exit(1)
    return jira


def fetch_jira_issue(jira: Any, jira_ticket: str) -> str:
    """Fetch JIRA issue and return its summary. Raises SystemExit on failure.

    Args:
        jira: JIRA client instance
        jira_ticket: JIRA ticket identifier (e.g., 'PROJ-123')

    Returns:
        Issue summary text
    """
    try:
        issue = jira.issue(jira_ticket)  # type: ignore[no-untyped-call]
        summary: str = issue.fields.summary  # type: ignore[no-untyped-call]
        print(f"[OK] Found ticket: {jira_ticket} - {summary}")
        return summary
    except (OSError, subprocess.SubprocessError) as e:
        print(f"[ERROR] Failed to fetch JIRA ticket {jira_ticket}: {e}", file=sys.stderr)
        sys.exit(1)


def transition_jira_ticket(jira: Any, ticket: str, branch_name: str) -> bool:
    """Transition JIRA ticket to 'In Progress' state.

    Args:
        jira: JIRA client instance
        ticket: JIRA ticket identifier
        branch_name: Git branch name associated with the ticket

    Returns:
        True if transition successful, False otherwise
    """
    try:
        issue = jira.issue(ticket)
        transitions = jira.transitions(issue)
        in_progress_id = None
        for t in transitions:
            if "progress" in t["name"].lower():
                in_progress_id = t["id"]
                break
        if in_progress_id:
            jira.transition_issue(issue, in_progress_id)
            print(f"[OK] Transitioned {ticket} to In Progress")
        else:
            print(f"[WARNING] Could not find 'In Progress' transition for {ticket}", file=sys.stderr)
        jira.add_comment(issue, f"Started work on branch: {branch_name}")
        return True
    except (OSError, subprocess.SubprocessError):
        print("[WARNING] Failed to transition JIRA ticket", file=sys.stderr)
        return False


def transition_to_review_state(jira: Any, ticket: str, branch_name: str) -> bool:
    """Transition JIRA ticket to 'In Review' or similar state.

    Args:
        jira: JIRA client instance
        ticket: JIRA ticket identifier
        branch_name: Git branch name associated with the ticket

    Returns:
        True if transition successful, False otherwise
    """
    try:
        issue = jira.issue(ticket)
        transitions = jira.transitions(issue)
        review_id = None
        for t in transitions:
            name_lower = t["name"].lower()
            if "review" in name_lower or "code review" in name_lower:
                review_id = t["id"]
                break
        if review_id:
            jira.transition_issue(issue, review_id)
            print(f"[OK] Transitioned {ticket} to In Review")
        else:
            print(f"[WARNING] Could not find 'Review' transition for {ticket}", file=sys.stderr)
        jira.add_comment(issue, f"Pull request created for branch: {branch_name}")
        return True
    except (OSError, subprocess.SubprocessError) as e:
        print(f"[WARNING] Failed to transition JIRA ticket: {e}", file=sys.stderr)
        return False


def transition_to_done_state(jira: Any, ticket: str) -> bool:
    """Transition JIRA ticket to 'Done' or 'Closed' state.

    Args:
        jira: JIRA client instance
        ticket: JIRA ticket identifier

    Returns:
        True if transition successful, False otherwise
    """
    try:
        issue = jira.issue(ticket)
        transitions = jira.transitions(issue)
        done_id = None
        for t in transitions:
            name_lower = t["name"].lower()
            if "done" in name_lower or "close" in name_lower or "resolved" in name_lower:
                done_id = t["id"]
                break
        if done_id:
            jira.transition_issue(issue, done_id)
            print(f"[OK] Transitioned {ticket} to Done")
        else:
            print(f"[WARNING] Could not find 'Done' transition for {ticket}", file=sys.stderr)
        jira.add_comment(issue, "Work completed and merged.")
        return True
    except (OSError, subprocess.SubprocessError) as e:
        print(f"[WARNING] Failed to transition JIRA ticket: {e}", file=sys.stderr)
        return False
