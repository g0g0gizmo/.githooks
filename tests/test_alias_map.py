"""Tests for alias map integration.

Verifies that 'test' alias loads from ALIAS_MAP with sensible defaults
when git config doesn't have explicit repo settings.
"""

from githooks.core.constants import ALIAS_MAP, DEFAULT_ROOT_BRANCH, TEST_JIRA_SERVER, TEST_REPO_URL
from githooks.core.repo_helpers import load_repo_config


def test_alias_test_loads_from_config_map():
    """Loading repo config for alias 'test' yields config-based URL."""
    # Ensure alias exists
    assert "test" in ALIAS_MAP
    cfg = load_repo_config("test")
    assert cfg["url"] == TEST_REPO_URL
    # Git config may override defaults, or use config defaults
    assert cfg["root_branch"] in ("main", DEFAULT_ROOT_BRANCH)
    # Test alias uses test-specific jira server when git config present, else fallback
    assert cfg["jira_server"] in (TEST_JIRA_SERVER, TEST_JIRA_SERVER)
    assert cfg["branch_prefix"] == "feature/"
    assert "clone_to" in cfg and isinstance(cfg["clone_to"], str)
