#!/usr/bin/env python3
"""
Git Hooks Unified Installer
============================

Cross-platform installation script for Git hooks collection.
Supports local and global installation with virtual environment setup.

Usage:
    python install.py [--repo-path PATH] [--global] [--force] [--skip-deps] [--help]

Examples:
    python install.py                           # Install in current directory
    python install.py --repo-path /path/to/repo # Install in specific repository
    python install.py --global                  # Install globally for all repositories
    python install.py --force                   # Force reinstall, overwrite existing hooks
    python install.py --skip-deps               # Skip dependency installation
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

# Import runtime detector for dynamic runtime path discovery
sys.path.insert(0, str(Path(__file__).parent))
from githooks.core.runtime_detector import RuntimeCache

_colors = {"CYAN": "\033[96m", "GREEN": "\033[92m", "YELLOW": "\033[93m", "RED": "\033[91m", "BLUE": "\033[94m", "RESET": "\033[0m", "BOLD": "\033[1m"}
# Disable colors on Windows without ANSI support
if platform.system() == "Windows" and not os.environ.get("ANSICON"):
    try:
        import colorama

        colorama.init()
    except ImportError:
        _colors = {k: "" for k in _colors}


class GitHooksInstaller:
    """Main installer class for Git hooks.

    Manages installation of Git hooks to local repositories or globally for all repositories.
    Hooks are installed as executable dispatcher scripts that execute .hook files sequentially.

    Attributes:
        script_dir (Path): Directory containing hook source files
        repo_path (Path): Target repository path for local installation
        global_install (bool): Whether to install hooks globally
        force (bool): Whether to overwrite existing hooks
        skip_deps (bool): Whether to skip dependency installation
        hook_types (list): List of Git hook types to install
    """

    def __init__(self, repo_path: Optional[str] = None, global_install: bool = False, force: bool = False, skip_deps: bool = False):
        """Initialize Git hooks installer.

        Args:
            repo_path: Path to target repository. Defaults to current directory.
            global_install: If True, install hooks globally for all repositories.
            force: If True, overwrite existing hooks.
            skip_deps: If True, skip dependency installation (deprecated in v2.0).
        """
        self.script_dir = Path(__file__).parent.resolve()
        self.repo_path = Path(repo_path).resolve() if repo_path else Path.cwd()
        self.global_install = global_install
        self.force = force
        self.skip_deps = skip_deps

        # Initialize runtime cache for auto-detection
        cache_repo_path = self.repo_path if not global_install else None
        self.runtime_cache = RuntimeCache(repo_path=cache_repo_path)

        # Hook types to install
        self.hook_types = [
            "pre-commit",
            "prepare-commit-msg",
            "commit-msg",
            "post-commit",
            "pre-push",
            "post-checkout",
            "pre-rebase",
            "post-rewrite",
            "pre-auto-gc",
            "post-receive",
            "pre-receive",
            "post-update",
            "applypatch-msg",
        ]

    def print_header(self, text: str) -> None:
        """Print a section header."""
        print()
        print(f"{_colors['CYAN']}{'=' * 70}{_colors['RESET']}")
        print(f"{_colors['CYAN']}  {text}{_colors['RESET']}")
        print(f"{_colors['CYAN']}{'=' * 70}{_colors['RESET']}")
        print()

    def print_step(self, text: str) -> None:
        """Print a step header."""
        print()
        print(f"{_colors['YELLOW']}{text}{_colors['RESET']}")
        print(f"{_colors['YELLOW']}{'-' * len(text)}{_colors['RESET']}")

    def print_success(self, text: str) -> None:
        """Print a success message."""
        print(f"{_colors['GREEN']}[OK] {text}{_colors['RESET']}")

    def print_info(self, text: str) -> None:
        """Print an info message."""
        print(f"{_colors['BLUE']}[i] {text}{_colors['RESET']}")

    def print_warning(self, text: str) -> None:
        """Print a warning message."""
        print(f"{_colors['YELLOW']}[!] {text}{_colors['RESET']}")

    def print_error(self, text: str) -> None:
        """Print an error message."""
        print(f"{_colors['RED']}[ERROR] {text}{_colors['RESET']}")

    def check_command_exists(self, command: str) -> bool:
        """Check if a command exists in system PATH.

        Args:
            command: Name of command to check (e.g., 'git', 'python3')

        Returns:
            True if command is found in PATH, False otherwise.
        """
        return shutil.which(command) is not None

    def get_version(self, command: List[str]) -> Optional[str]:
        """Get version string from a command.

        Args:
            command: Command and arguments as list (e.g., ['git', '--version'])

        Returns:
            Version string from command stdout, or None if command fails.
        """
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    def check_prerequisites(self) -> bool:
        """Check all installation prerequisites are met.

        Validates:
            - Python 3.9+ is installed
            - Git 2.0+ is available in PATH
            - Optional tools (dotenvx, Maven) if present

        Prints status messages for each prerequisite.

        Returns:
            True if all required prerequisites met, False otherwise.
        """
        self.print_step("Validating Prerequisites")

        all_ok = True

        # Check Python version
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        if sys.version_info < (3, 9):
            self.print_error(f"Python 3.9+ required, found {python_version}")
            all_ok = False
        else:
            self.print_success(f"Python {python_version}")

        # Check Git
        if not self.check_command_exists("git"):
            self.print_error("Git not found in PATH")
            all_ok = False
        else:
            git_version = self.get_version(["git", "--version"])
            self.print_success(f"Git {git_version}")

        # Check optional dependencies
        if self.check_command_exists("dotenvx"):
            dotenvx_version = self.get_version(["dotenvx", "--version"])
            self.print_success(f"dotenvx {dotenvx_version}")
        else:
            self.print_warning("dotenvx not found (optional - required for dotenvx.hook)")

        if self.check_command_exists("mvn"):
            mvn_version = self.get_version(["mvn", "--version"])
            if mvn_version:
                mvn_version = mvn_version.split("\n")[0]  # First line only
            self.print_success(f"Maven {mvn_version}")
        else:
            self.print_warning("Maven not found (optional - required for some hooks)")

        return all_ok

    def is_git_repository(self, path: Path) -> bool:
        """Check if a directory is a Git repository.

        Args:
            path: Directory path to check

        Returns:
            True if directory contains .git subdirectory, False otherwise.
        """
        git_dir = path / ".git"
        return git_dir.exists()

    def install_local_hooks(self) -> bool:
        """Install hooks to a local Git repository.

        Creates dispatcher hooks in .git/hooks/ directory for each hook type.
        Each dispatcher executes all .hook files in the corresponding source directory.

        Returns:
            True if installation succeeded, False if repository validation failed.

        Prints:
            Installation progress and count of installed hooks.
        """
        self.print_step("Installing Git Hooks (Local)")

        # Validate repository
        if not self.is_git_repository(self.repo_path):
            self.print_error(f"Not a Git repository: {self.repo_path}")
            return False

        hooks_dir = self.repo_path / ".git" / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)

        self.print_info(f"Repository: {self.repo_path}")
        self.print_info(f"Hooks directory: {hooks_dir}")

        # Install each hook type
        installed_count = 0
        for hook_type in self.hook_types:
            source_dir = self.script_dir / hook_type
            if not source_dir.exists():
                continue

            hook_file = hooks_dir / hook_type
            if hook_file.exists() and not self.force:
                self.print_warning(f"Hook already exists (skipping): {hook_type}")
                continue

            # Create dispatcher hook that calls all .hook files in the directory
            hook_content = self._generate_dispatcher_hook(hook_type, local=True)
            hook_file.write_text(hook_content, encoding="utf-8")

            # Make executable on Unix-like systems
            if platform.system() != "Windows":
                hook_file.chmod(0o755)

            self.print_success(f"Installed: {hook_type}")
            installed_count += 1

        self.print_info(f"Installed {installed_count} hook(s)")
        return True

    def install_global_hooks(self) -> bool:
        """Install hooks globally for all Git repositories on system.

        Creates hooks in ~/.git-hooks/ directory and configures Git to use them
        via core.hooksPath setting. Affects all repositories for current user.

        Returns:
            True if installation succeeded, False if Git config failed.

        Raises:
            subprocess.CalledProcessError: If git config command fails.
        """
        self.print_step("Installing Git Hooks (Global)")

        # Determine global hooks directory
        global_hooks_dir = Path.home() / ".git-hooks"
        global_hooks_dir.mkdir(parents=True, exist_ok=True)
        self.print_info(f"Global hooks directory: {global_hooks_dir}")

        # Configure Git to use global hooks directory
        try:
            subprocess.run(["git", "config", "--global", "core.hooksPath", str(global_hooks_dir)], check=True, capture_output=True)
            self.print_success("Configured Git to use global hooks directory")
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to configure Git: {e}")
            return False

        # Install each hook type
        installed_count = 0
        for hook_type in self.hook_types:
            source_dir = self.script_dir / hook_type
            if not source_dir.exists():
                continue

            hook_file = global_hooks_dir / hook_type
            if hook_file.exists() and not self.force:
                self.print_warning(f"Hook already exists (skipping): {hook_type}")
                continue

            # Create dispatcher hook
            hook_content = self._generate_dispatcher_hook(hook_type, local=False)
            hook_file.write_text(hook_content, encoding="utf-8")

            # Make executable on Unix-like systems
            if platform.system() != "Windows":
                hook_file.chmod(0o755)

            self.print_success(f"Installed: {hook_type}")
            installed_count += 1

        self.print_info(f"Installed {installed_count} hook(s)")
        return True

    def _generate_dispatcher_hook(self, hook_type: str, local: bool = True) -> str:
        """Generate Python dispatcher hook script content.

        Creates a Python script that:
        1. Finds all .hook files in the hook type directory
        2. Executes each hook as a subprocess sequentially
        3. Stops on first failure (non-zero exit code)

        Args:
            hook_type: Git hook type (e.g., 'pre-commit', 'commit-msg')
            local: If True, use local paths. If False, use global paths.

        Returns:
            Complete Python script as string with shebang and hook execution logic.

        Security:
            Uses subprocess.run() with shell=False for safe execution.
            No exec() or eval() calls.
        """
        if local:
            hooks_source_dir = self.script_dir / hook_type
        else:
            hooks_source_dir = self.script_dir / hook_type

        # Use shebang to find Python in user's environment
        # Use 'python' instead of 'python3' for Windows compatibility
        shebang = "#!/usr/bin/env python"

        # Detect runtime paths using RuntimeCache
        python_path = self.runtime_cache.get_python_path()
        bash_path = self.runtime_cache.get_bash_path()

        # Escape paths for inclusion in Python f-string
        python_path_escaped = python_path.replace("\\", "\\\\")
        bash_path_escaped = bash_path.replace("\\", "\\\\") if bash_path else "bash"

        return f'''{shebang}
"""
{hook_type} hook - Dispatcher
Auto-generated by install.py
Executes all .hook files in {hook_type}/ directory sequentially.
"""
import sys
import os
from pathlib import Path
import subprocess
import platform

# Add repo root to Python path so hooks can import from githooks module
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

# Runtime paths detected at installation time
PYTHON_PATH = r'{python_path_escaped}'
BASH_PATH = r'{bash_path_escaped}'

hooks_dir = Path(r'{hooks_source_dir}')
hook_files = sorted(hooks_dir.glob('*.hook'))

exit_code = 0
for hook_file in hook_files:
    if not hook_file.is_file():
        continue
    # Skip dispatcher.hook to avoid recursion
    if hook_file.name == 'dispatcher.hook':
        continue
    # Skip disabled hooks
    if hook_file.name.endswith('.disabled'):
        continue

    try:
        # Read first line to determine how to execute
        with open(hook_file, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()

        # Convert path to string
        hook_path = str(hook_file)

        # Determine execution method based on shebang
        if first_line.startswith('#!') and 'python' in first_line:
            # Python hook - use detected Python path
            cmd = [PYTHON_PATH, hook_path] + sys.argv[1:]
        elif first_line.startswith('#!') and ('bash' in first_line or 'sh' in first_line):
            # Shell/bash hook
            if platform.system() == 'Windows':
                # Use detected Git Bash path
                # Verify bash still exists, fallback to PATH search
                bash_exe = BASH_PATH if Path(BASH_PATH).exists() else 'bash'
                # Convert backslashes to forward slashes for bash
                hook_path_bash = hook_path.replace('\\\\', '/')
                cmd = [bash_exe, hook_path_bash] + sys.argv[1:]
            else:
                cmd = [hook_path] + sys.argv[1:]
        else:
            # Unknown - try executing directly
            cmd = [hook_path] + sys.argv[1:]

        result = subprocess.run(cmd, shell=False, check=False, capture_output=True, encoding="utf-8", errors="replace")

        if result.returncode != 0:
            print(result.stdout, file=sys.stdout, end='')
            print(result.stderr, file=sys.stderr, end='')
            exit_code = result.returncode
            break
    except Exception as e:
        print(f'Error executing {{hook_file.name}}: {{e}}', file=sys.stderr)
        exit_code = 1
        break

sys.exit(exit_code)
'''

    def print_summary(self) -> None:
        """Print installation summary and next steps.

        Displays:
            - Installation completion message
            - Next steps for user
            - Note about Python environment usage
        """
        self.print_header("Installation Complete!")

        print(f"{_colors['YELLOW']}Next steps:{_colors['RESET']}")
        print("1. Hooks are now active and will run automatically on Git events")

        if self.global_install:
            print("2. Your hooks are installed globally for all Git repositories")
        else:
            print(f"2. Your hooks are installed in: {self.repo_path}")

        print()
        print(f"{_colors['BLUE']}Note:{_colors['RESET']} Hooks use your current Python environment (system or project venv)")
        print()

    def run(self) -> int:
        """Run the complete installation workflow.

        Workflow:
            1. Print header
            2. Check prerequisites
            3. Install hooks (local or global based on configuration)
            4. Print summary

        Returns:
            0 if installation succeeded, 1 if failed.

        Example:
            >>> installer = GitHooksInstaller(repo_path='/path/to/repo')
            >>> exit_code = installer.run()
            >>> sys.exit(exit_code)
        """
        self.print_header("Git Hooks Installer")

        # Check prerequisites
        if not self.check_prerequisites():
            self.print_error("Prerequisites check failed. Please install missing dependencies.")
            return 1

        # Install hooks
        if self.global_install:
            if not self.install_global_hooks():
                self.print_error("Global hooks installation failed.")
                return 1
        else:
            if not self.install_local_hooks():
                self.print_error("Local hooks installation failed.")
                return 1

        # Print summary
        self.print_summary()

        return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Git Hooks Unified Installer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python install.py                           # Install in current directory
  python install.py --repo-path /path/to/repo # Install in specific repository
  python install.py --global                  # Install globally for all repositories
  python install.py --force                   # Force reinstall, overwrite existing hooks
  python install.py --skip-deps               # Skip dependency installation
  python install.py --force-detect            # Force re-detection of runtime paths
""",
    )

    parser.add_argument("--repo-path", type=str, default=None, help="Path to Git repository (default: current directory)")
    parser.add_argument("--global", dest="global_install", action="store_true", help="Install hooks globally for all repositories")
    parser.add_argument("--force", action="store_true", help="Force reinstall, overwriting existing hooks")
    parser.add_argument("--skip-deps", action="store_true", help="Skip Python dependency installation")
    parser.add_argument("--force-detect", action="store_true", help="Force re-detection of runtime paths (bash, python, node)")

    args = parser.parse_args()

    installer = GitHooksInstaller(repo_path=args.repo_path, global_install=args.global_install, force=args.force, skip_deps=args.skip_deps)

    # Force runtime detection if requested
    if args.force_detect:
        installer.runtime_cache.invalidate()
        installer.print_info("Invalidated runtime cache - will re-detect bash, python, node")

    try:
        return installer.run()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        return 130
    except (OSError, ValueError, RuntimeError) as e:
        # Catch common runtime errors; specific exceptions are handled above.
        print(f"\n\nUnexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
