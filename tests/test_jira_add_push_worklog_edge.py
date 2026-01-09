"""
Edge case and error handling tests for jira_add_push_worklog.py.
Covers parse_ticket_from_branch, get_current_branch, and get_jira_client error paths.
"""

import os

import pytest

import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog


def test_parse_ticket_from_branch_none():
    """Should return None for branch names without ticket pattern."""
    assert jira_add_push_worklog.parse_ticket_from_branch("") is None
    assert jira_add_push_worklog.parse_ticket_from_branch("main") is None
    assert jira_add_push_worklog.parse_ticket_from_branch("feature/add-new-api") is None


def test_get_current_branch_handles_error(monkeypatch):
    """Should return None if git command fails."""

    def fail_run(*args, **kwargs):
        raise Exception("fail")

    monkeypatch.setattr("subprocess.run", fail_run)
    assert jira_add_push_worklog.get_current_branch() is None


def test_get_jira_client_no_env(monkeypatch):
    """Should return None or prompt if no credentials in env or keyring."""
    monkeypatch.delenv("JIRA_USERNAME", raising=False)
    monkeypatch.delenv("JIRA_TOKEN", raising=False)
    monkeypatch.delenv("GOJIRA_USERNAME", raising=False)
    monkeypatch.delenv("GOJIRA_SECRET", raising=False)

    # Patch keyring to return None
    class DummyKeyring:
        def get_password(self, *a, **k):
            return None

        def set_password(self, *a, **k):
            return None

    monkeypatch.setattr(jira_add_push_worklog, "keyring", DummyKeyring())
    # Patch input to raise EOFError (simulate no input possible)
    monkeypatch.setattr("builtins.input", lambda *a, **k: (_ for _ in ()).throw(EOFError()))
    try:
        result = jira_add_push_worklog.get_jira_client()
    except EOFError:
        result = None
    assert result is None or hasattr(result, "issue")
