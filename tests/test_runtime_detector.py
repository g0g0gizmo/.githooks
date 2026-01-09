#!/usr/bin/env python
"""Tests for runtime detection and caching.

Verifies cross-platform runtime detection for bash, Python, and Node.js
with Git config-backed caching.
"""

import platform
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from githooks.core.runtime_detector import BashDetector, NodeDetector, PythonDetector, RuntimeCache


class TestBashDetector:
    """Tests for bash executable detection."""

    def test_detect_returns_valid_path(self):
        """BashDetector.detect() returns an existing executable path."""
        bash_path = BashDetector.detect()

        # Bash or sh should be found on most systems
        assert bash_path is not None
        assert Path(bash_path).exists()

    @pytest.mark.skipif(platform.system() != "Windows", reason="Windows-specific test")
    def test_detect_windows_finds_git_bash(self):
        """On Windows, detector finds Git Bash in standard location."""
        bash_path = BashDetector._detect_windows()

        # Should find bash.exe or sh.exe
        assert bash_path is not None
        assert bash_path.endswith((".exe", "bash", "sh"))

    @pytest.mark.skipif(platform.system() == "Windows", reason="Unix-specific test")
    def test_detect_unix_finds_bash(self):
        """On Unix systems, detector finds bash in standard locations."""
        bash_path = BashDetector._detect_unix()

        assert bash_path is not None
        # Should be one of the standard paths
        assert any(path in bash_path for path in ["/bin/bash", "/usr/bin/bash", "/usr/local/bin/bash"])

    def test_detect_bash_is_executable(self):
        """Detected bash path points to an executable file."""
        bash_path = BashDetector.detect()

        if bash_path:
            # Verify it's actually executable
            result = subprocess.run([bash_path, "--version"], capture_output=True, text=True, timeout=5)
            assert result.returncode == 0
            assert "bash" in result.stdout.lower() or "sh" in result.stdout.lower()


class TestPythonDetector:
    """Tests for Python interpreter detection."""

    def test_detect_returns_current_python(self):
        """PythonDetector.detect() returns path to current Python interpreter."""
        python_path = PythonDetector.detect()

        assert python_path is not None
        assert Path(python_path).exists()

    def test_detect_python_is_executable(self):
        """Detected Python path is executable and responds to --version."""
        python_path = PythonDetector.detect()

        result = subprocess.run([python_path, "--version"], capture_output=True, text=True, timeout=5)
        assert result.returncode == 0
        assert "Python" in result.stdout or "Python" in result.stderr


class TestNodeDetector:
    """Tests for Node.js runtime detection."""

    def test_detect_returns_none_or_valid_path(self):
        """NodeDetector.detect() returns None or a valid node executable."""
        node_path = NodeDetector.detect()

        # Node is optional, so None is acceptable
        if node_path is not None:
            assert Path(node_path).exists()

    def test_detect_node_is_executable_when_found(self):
        """When Node.js is detected, it responds to --version."""
        node_path = NodeDetector.detect()

        if node_path:
            result = subprocess.run([node_path, "--version"], capture_output=True, text=True, timeout=5)
            assert result.returncode == 0
            # Node version output starts with 'v'
            assert result.stdout.strip().startswith("v")


class TestRuntimeCache:
    """Tests for Git config-backed runtime caching."""

    def test_cache_stores_and_retrieves_bash_path(self, temp_git_repo):
        """RuntimeCache caches bash path in Git config."""
        cache = RuntimeCache(repo_path=temp_git_repo)

        # First call should detect and cache
        bash_path = cache.get_bash_path(force_detect=True)
        assert bash_path is not None

        # Second call should retrieve from cache
        cached_path = cache.get_bash_path()
        assert cached_path == bash_path

    def test_cache_stores_and_retrieves_python_path(self, temp_git_repo):
        """RuntimeCache caches Python path in Git config."""
        cache = RuntimeCache(repo_path=temp_git_repo)

        python_path = cache.get_python_path(force_detect=True)
        assert python_path is not None

        cached_path = cache.get_python_path()
        assert cached_path == python_path

    def test_cache_invalidation_clears_all_entries(self, temp_git_repo):
        """RuntimeCache.invalidate() removes all cached runtime paths."""
        cache = RuntimeCache(repo_path=temp_git_repo)

        # Cache some values
        cache.get_bash_path(force_detect=True)
        cache.get_python_path(force_detect=True)

        # Invalidate
        cache.invalidate()

        # Verify cache keys are gone (use --local to check local config only)
        result = subprocess.run(
            ["git", "config", "--local", "hooks.runtime.bash"],
            cwd=temp_git_repo,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode != 0  # Key should not exist in local config

    def test_cache_respects_ttl(self, temp_git_repo):
        """RuntimeCache respects time-to-live for cache entries."""
        # Create cache with very short TTL
        cache = RuntimeCache(repo_path=temp_git_repo, cache_ttl=timedelta(seconds=0))

        # Cache a value
        cache.get_bash_path(force_detect=True)

        # With 0-second TTL, cache should be immediately invalid
        # This should trigger re-detection
        with patch.object(BashDetector, "detect", return_value="/fake/bash") as mock_detect:
            cache.get_bash_path()
            # Should have called detect again because cache expired
            mock_detect.assert_called_once()

    def test_cache_redetects_if_path_missing(self, temp_git_repo):
        """RuntimeCache re-detects if cached path no longer exists."""
        cache = RuntimeCache(repo_path=temp_git_repo)

        # Manually set a fake cached path
        cache._git_config_set("hooks.runtime.bash", "/nonexistent/bash")
        cache._git_config_set("hooks.runtime.detectedAt", datetime.now().isoformat())

        # get_bash_path should detect path is invalid and re-detect
        bash_path = cache.get_bash_path()

        # Should have re-detected and found real bash
        assert bash_path is not None
        assert bash_path != "/nonexistent/bash"
        assert Path(bash_path).exists()

    def test_force_detect_bypasses_cache(self, temp_git_repo):
        """force_detect parameter bypasses cache and re-detects."""
        cache = RuntimeCache(repo_path=temp_git_repo)

        # Cache a value
        original_path = cache.get_bash_path(force_detect=True)

        # Force detection should call detector even with valid cache
        with patch.object(BashDetector, "detect", return_value=original_path) as mock_detect:
            cache.get_bash_path(force_detect=True)
            mock_detect.assert_called_once()

    def test_cache_timestamp_updated_on_write(self, temp_git_repo):
        """RuntimeCache updates detectedAt timestamp when caching."""
        cache = RuntimeCache(repo_path=temp_git_repo)

        before = datetime.now()
        cache.get_bash_path(force_detect=True)
        after = datetime.now()

        # Check timestamp was written
        timestamp_str = cache._git_config_get("hooks.runtime.detectedAt")
        assert timestamp_str is not None

        timestamp = datetime.fromisoformat(timestamp_str)
        assert before <= timestamp <= after

    def test_cache_works_with_global_config(self):
        """RuntimeCache works with global Git config when repo_path is None."""
        cache = RuntimeCache(repo_path=None)

        try:
            # This should use --global flag
            bash_path = cache.get_bash_path(force_detect=True)
            assert bash_path is not None

            # Verify it was written to global config
            result = subprocess.run(
                ["git", "config", "--global", "hooks.runtime.bash"],
                capture_output=True,
                text=True,
                check=False,
            )
            assert result.returncode == 0
            assert result.stdout.strip() == bash_path
        finally:
            # Clean up global config
            cache.invalidate()


class TestCrossPlatformCompatibility:
    """Tests verifying runtime detection works across platforms."""

    @pytest.mark.parametrize(
        "detector_class,runtime_name",
        [
            (BashDetector, "bash"),
            (PythonDetector, "python"),
        ],
    )
    def test_detector_works_on_current_platform(self, detector_class, runtime_name):
        """Required runtime detectors work on current platform."""
        detected_path = detector_class.detect()

        assert detected_path is not None, f"{runtime_name} should be detected on {platform.system()}"
        assert Path(detected_path).exists()

    def test_runtime_cache_integration(self, temp_git_repo):
        """Full integration test of RuntimeCache with all runtimes."""
        cache = RuntimeCache(repo_path=temp_git_repo)

        # Detect all runtimes
        bash = cache.get_bash_path(force_detect=True)
        python = cache.get_python_path(force_detect=True)
        node = cache.get_node_path(force_detect=True)

        # Bash and Python are required
        assert bash is not None
        assert python is not None
        # Node is optional

        # Verify all cached values can be retrieved
        assert cache.get_bash_path() == bash
        assert cache.get_python_path() == python
        if node:
            assert cache.get_node_path() == node
