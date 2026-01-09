#!/usr/bin/env python
"""Runtime Detection and Caching for Git Hooks.

This module provides automatic detection and caching of runtime dependencies
(bash, python, node) across platforms. Detection results are cached in Git config
to avoid repeated lookups on every hook execution.

Key Features:
    - Cross-platform runtime detection (Windows, macOS, Linux)
    - Git config-backed caching with invalidation
    - Fallback chains for maximum compatibility
    - Sub-100ms performance with caching

Classes:
    BashDetector: Detect bash executable on all platforms
    PythonDetector: Resolve Python interpreter path
    NodeDetector: Find Node.js runtime
    RuntimeCache: Manage cached runtime paths in Git config

Example:
    >>> from githooks.core.runtime_detector import RuntimeCache
    >>> cache = RuntimeCache()
    >>> bash_path = cache.get_bash_path()
    >>> print(f"Bash found at: {bash_path}")
"""

import os
import platform
import shutil
import subprocess
import winreg
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


class BashDetector:
    """Detect bash executable with platform-specific fallback chains.

    Detection Order (Windows):
        1. Git Bash: C:\\Program Files\\Git\\bin\\bash.exe
        2. Git registry: HKLM\\SOFTWARE\\GitForWindows\\InstallPath
        3. Scoop: %USERPROFILE%\\scoop\\apps\\git\\current\\bin\\bash.exe
        4. Chocolatey: C:\\ProgramData\\chocolatey\\bin\\bash.exe
        5. PATH search: which bash
        6. Fallback: sh

    Detection Order (Unix):
        1. which bash
        2. /bin/bash
        3. /usr/bin/bash
        4. /usr/local/bin/bash
        5. Fallback: sh
    """

    @staticmethod
    def detect() -> Optional[str]:
        """Detect bash executable path.

        Returns:
            Absolute path to bash executable, or None if not found.

        Example:
            >>> bash_path = BashDetector.detect()
            >>> print(bash_path)
            'C:\\Program Files\\Git\\bin\\bash.exe'
        """
        system = platform.system()

        if system == "Windows":
            return BashDetector._detect_windows()
        else:
            return BashDetector._detect_unix()

    @staticmethod
    def _detect_windows() -> Optional[str]:
        """Detect bash on Windows with comprehensive fallback chain."""
        # 1. Standard Git for Windows installation
        standard_path = Path(r"C:\Program Files\Git\bin\bash.exe")
        if standard_path.exists():
            return str(standard_path)

        # 2. Check Windows registry for Git installation
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\GitForWindows") as key:
                install_path = winreg.QueryValueEx(key, "InstallPath")[0]
                bash_path = Path(install_path) / "bin" / "bash.exe"
                if bash_path.exists():
                    return str(bash_path)
        except (OSError, FileNotFoundError):
            pass

        # 3. Scoop package manager
        scoop_path = Path.home() / "scoop" / "apps" / "git" / "current" / "bin" / "bash.exe"
        if scoop_path.exists():
            return str(scoop_path)

        # 4. Chocolatey package manager
        choco_path = Path(r"C:\ProgramData\chocolatey\bin\bash.exe")
        if choco_path.exists():
            return str(choco_path)

        # 5. PATH search using shutil.which
        bash_in_path = shutil.which("bash")
        if bash_in_path:
            return bash_in_path

        # 6. Fallback to sh (less features but usually works)
        sh_in_path = shutil.which("sh")
        if sh_in_path:
            return sh_in_path

        return None

    @staticmethod
    def _detect_unix() -> Optional[str]:
        """Detect bash on Unix-like systems."""
        # 1. Use which command
        bash_in_path = shutil.which("bash")
        if bash_in_path:
            return bash_in_path

        # 2. Common installation paths
        common_paths = ["/bin/bash", "/usr/bin/bash", "/usr/local/bin/bash"]
        for path_str in common_paths:
            path = Path(path_str)
            if path.exists() and os.access(path, os.X_OK):
                return str(path)

        # 3. Fallback to sh
        sh_in_path = shutil.which("sh")
        if sh_in_path:
            return sh_in_path

        return None


class PythonDetector:
    """Resolve Python interpreter path for hook execution.

    Uses sys.executable to ensure consistency with the Python
    running the installer/hooks.
    """

    @staticmethod
    def detect() -> str:
        """Detect Python interpreter path.

        Returns:
            Absolute path to Python executable.

        Raises:
            RuntimeError: If Python executable cannot be determined.
        """
        import sys

        python_path = sys.executable
        if not python_path or not Path(python_path).exists():
            raise RuntimeError("Cannot determine Python executable path")
        return python_path


class NodeDetector:
    """Find Node.js runtime for JavaScript-based hooks.

    Detection Order:
        1. PATH search: which node
        2. Common Windows paths: C:\\Program Files\\nodejs\\node.exe
        3. NVM installations
        4. None if not found (optional dependency)
    """

    @staticmethod
    def detect() -> Optional[str]:
        """Detect Node.js executable path.

        Returns:
            Absolute path to node executable, or None if not found.
            Node.js is optional - hooks requiring it should degrade gracefully.
        """
        # 1. PATH search
        node_in_path = shutil.which("node")
        if node_in_path:
            return node_in_path

        # 2. Windows common paths
        if platform.system() == "Windows":
            common_paths = [
                Path(r"C:\Program Files\nodejs\node.exe"),
                Path(r"C:\Program Files (x86)\nodejs\node.exe"),
            ]
            for path in common_paths:
                if path.exists():
                    return str(path)

        return None


class RuntimeCache:
    """Manage cached runtime paths in Git config.

    Caches runtime detection results to avoid repeated filesystem
    searches on every hook execution. Cache invalidation happens
    automatically if paths become invalid or after 7 days.

    Git Config Keys:
        hooks.runtime.bash: Cached bash path
        hooks.runtime.python: Cached Python path
        hooks.runtime.node: Cached Node.js path
        hooks.runtime.detectedAt: ISO timestamp of last detection

    Attributes:
        repo_path: Repository path for local config, None for global
        cache_ttl: Time-to-live for cache entries (default: 7 days)
    """

    def __init__(self, repo_path: Optional[Path] = None, cache_ttl: timedelta = timedelta(days=7)):
        """Initialize runtime cache.

        Args:
            repo_path: Repository path for local config. If None, uses global config.
            cache_ttl: Cache time-to-live. Default: 7 days.
        """
        self.repo_path = repo_path
        self.cache_ttl = cache_ttl

    def get_bash_path(self, force_detect: bool = False) -> Optional[str]:
        """Get bash path from cache or detect.

        Args:
            force_detect: If True, bypass cache and re-detect.

        Returns:
            Absolute path to bash executable.
        """
        if not force_detect:
            cached_path = self._read_cache("bash")
            if cached_path and self._is_cache_valid() and self._path_exists(cached_path):
                return cached_path

        # Cache miss or invalid - detect and cache
        detected_path = BashDetector.detect()
        if detected_path:
            self._write_cache("bash", detected_path)
        return detected_path

    def get_python_path(self, force_detect: bool = False) -> str:
        """Get Python path from cache or detect.

        Args:
            force_detect: If True, bypass cache and re-detect.

        Returns:
            Absolute path to Python executable.

        Raises:
            RuntimeError: If Python cannot be detected.
        """
        if not force_detect:
            cached_path = self._read_cache("python")
            if cached_path and self._is_cache_valid() and self._path_exists(cached_path):
                return cached_path

        detected_path = PythonDetector.detect()
        self._write_cache("python", detected_path)
        return detected_path

    def get_node_path(self, force_detect: bool = False) -> Optional[str]:
        """Get Node.js path from cache or detect.

        Args:
            force_detect: If True, bypass cache and re-detect.

        Returns:
            Absolute path to node executable, or None if not found.
        """
        if not force_detect:
            cached_path = self._read_cache("node")
            if cached_path and self._is_cache_valid() and self._path_exists(cached_path):
                return cached_path

        detected_path = NodeDetector.detect()
        if detected_path:
            self._write_cache("node", detected_path)
        return detected_path

    def invalidate(self) -> None:
        """Invalidate all cached runtime paths.

        Forces re-detection on next access. Useful when runtime
        environments change (e.g., Git reinstalled).
        """
        for key in ["bash", "python", "node", "detectedAt"]:
            self._git_config_unset(f"hooks.runtime.{key}")

    def _read_cache(self, runtime: str) -> Optional[str]:
        """Read cached runtime path from Git config."""
        return self._git_config_get(f"hooks.runtime.{runtime}")

    def _write_cache(self, runtime: str, path: str) -> None:
        """Write runtime path to Git config cache."""
        self._git_config_set(f"hooks.runtime.{runtime}", path)
        # Update timestamp
        timestamp = datetime.now().isoformat()
        self._git_config_set("hooks.runtime.detectedAt", timestamp)

    def _is_cache_valid(self) -> bool:
        """Check if cache is within TTL."""
        timestamp_str = self._git_config_get("hooks.runtime.detectedAt")
        if not timestamp_str:
            return False

        try:
            timestamp = datetime.fromisoformat(timestamp_str)
            age = datetime.now() - timestamp
            return age < self.cache_ttl
        except (ValueError, TypeError):
            return False

    def _path_exists(self, path: str) -> bool:
        """Verify cached path still exists."""
        return Path(path).exists()

    def _git_config_get(self, key: str) -> Optional[str]:
        """Read value from Git config."""
        cmd = ["git", "config"]
        if self.repo_path:
            cmd.append("--local")
        else:
            cmd.append("--global")
        cmd.append(key)

        try:
            result = subprocess.run(cmd, cwd=self.repo_path, capture_output=True, text=True, check=False, encoding="utf-8", errors="replace")
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.SubprocessError, OSError):
            pass
        return None

    def _git_config_set(self, key: str, value: str) -> None:
        """Write value to Git config."""
        cmd = ["git", "config"]
        if self.repo_path:
            cmd.append("--local")
        else:
            cmd.append("--global")
        cmd.extend([key, value])

        try:
            subprocess.run(cmd, cwd=self.repo_path, check=True, capture_output=True, encoding="utf-8", errors="replace")
        except (subprocess.SubprocessError, OSError) as exc:
            # Non-fatal - cache write failure shouldn't break installation
            print(f"Warning: Failed to cache runtime path: {exc}")

    def _git_config_unset(self, key: str) -> None:
        """Remove value from Git config."""
        cmd = ["git", "config"]
        if self.repo_path:
            cmd.append("--local")
        else:
            cmd.append("--global")
        cmd.extend(["--unset", key])

        try:
            subprocess.run(cmd, cwd=self.repo_path, check=False, capture_output=True, encoding="utf-8", errors="replace")
        except (subprocess.SubprocessError, OSError):
            pass  # Ignore errors - key might not exist
