"""
Low-level JIRA client and authentication utilities.

This module provides stateless foundational functions for JIRA integration:
- Credential retrieval (environment variables, system keyring, or interactive prompts)
- Authenticated JIRA client instance creation
- Ticket key parsing from branch names

This is the bottom layer of the JIRA integration stack. It has no knowledge of
git-go workflows or business logic - it only handles authentication and client setup.

Architecture:
    CLI Commands → jira_helpers (business logic) → jira_client (this module)

Credentials are sourced from environment variables, system keyring, or user input,
and can be cached securely using the keyring library.
"""

import getpass
import os
import re
import sys
from typing import Optional

import keyring
from jira import JIRA

from githooks.core.constants import BRANCH_REGEX, DEFAULT_JIRA_SERVER, SERVICE_NAME


def get_jira_credentials() -> tuple[str, str]:
    """
    Retrieve JIRA username and API token from environment, keyring, or user input.

    Returns:
        tuple[str, str]: A tuple containing the JIRA username/email and API token.
    """
    username = os.environ.get("JIRA_USERNAME") or os.environ.get("GOJIRA_USERNAME")
    token = os.environ.get("JIRA_TOKEN") or os.environ.get("GOJIRA_SECRET")
    if not username:
        username = keyring.get_password(f"{SERVICE_NAME}.jira.username", "username")  # type: ignore[union-attr]
    if not token:
        token = keyring.get_password(f"{SERVICE_NAME}.jira.password", "password")  # type: ignore[union-attr]
    if not username:
        username = input("Enter your Jira username/email: ")
        keyring.set_password(f"{SERVICE_NAME}.jira.username", "username", username)  # type: ignore[union-attr]
    if not token:
        token = getpass.getpass("Enter Jira API token: ")
        keyring.set_password(f"{SERVICE_NAME}.jira.password", "password", token)  # type: ignore[union-attr]
    return username, token


def get_jira_client(server: Optional[str] = None):
    """
    Create and return a JIRA client instance using provided or default server.

    Parameters:
        server (Optional[str]): The JIRA server URL. If None, uses the default server.

    Returns:
        JIRA: An authenticated JIRA client instance, or None if creation fails.
    """
    username, token = get_jira_credentials()
    jira_server = server or DEFAULT_JIRA_SERVER
    try:
        auth: Optional[tuple[str, str]] = (username, token) if username and token else None
        return JIRA(server=jira_server, basic_auth=auth)
    except Exception as e:
        # Catching general Exception is not ideal, but JIRA client can raise various errors
        print(f"[ERROR] Failed to create Jira client: {e}", file=sys.stderr)
        return None


def parse_ticket_from_branch(branch: str) -> Optional[str]:
    """
    Parse and return the JIRA ticket key from a branch name using the configured regex.

    Parameters:
        branch (str): The branch name to parse.

    Returns:
        Optional[str]: The extracted JIRA ticket key, or None if not found.
    """

    match = re.search(BRANCH_REGEX, branch)
    return match.group(1) if match else None
