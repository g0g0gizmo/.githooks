"""Unit tests for GitHooksInstaller class.

Tests install.py functionality by importing the GitHooksInstaller class directly,
allowing pytest-cov to measure coverage. These complement integration tests which
run install.py as subprocess (functional verification but no coverage measurement).
"""

import platform
import subprocess
import sys
from pathlib import Path

import pytest

# Import installer for unit testing (not subprocess execution)
sys.path.insert(0, str(Path(__file__).parent.parent))
from install import GitHooksInstaller


def test_installer_initialization():
    """GitHooksInstaller initializes with correct defaults."""
    installer = GitHooksInstaller()

    # Script directory should exist (where install.py lives)
    assert installer.script_dir.exists(), "Script directory should exist"
    assert (installer.script_dir / "pre-commit").exists(), "pre-commit directory should exist"
    assert (installer.script_dir / "commit-msg").exists(), "commit-msg directory should exist"

    # Repo path should default to current directory
    assert installer.repo_path.is_absolute(), "Repo path should be absolute"

    # Flags should have default values
    assert installer.global_install is False, "global_install should default to False"
    assert installer.force is False, "force should default to False"
    assert installer.skip_deps is False, "skip_deps should default to False"


def test_installer_initialization_global():
    """GitHooksInstaller initializes with global_install=True."""
    installer = GitHooksInstaller(global_install=True)

    assert installer.global_install is True, "global_install should be True"


def test_generate_dispatcher_hook_local():
    """_generate_dispatcher_hook generates valid dispatcher hook for local install."""
    installer = GitHooksInstaller()

    # Generate dispatcher for pre-commit
    dispatcher_content = installer._generate_dispatcher_hook("pre-commit", local=True)

    # Verify structure
    assert "#!/usr/bin/env python" in dispatcher_content, "Should have python shebang (cross-platform)"
    assert "pre-commit" in dispatcher_content, "Should reference hook type"
    assert "subprocess.run" in dispatcher_content, "Should use subprocess.run for security"
    assert "sys.exit" in dispatcher_content, "Should exit with proper code"

    # Verify security: should NOT use exec() or eval()
    assert "exec(" not in dispatcher_content, "Should not use exec()"
    assert "eval" not in dispatcher_content, "Should not use eval"


def test_generate_dispatcher_hook_global():
    """_generate_dispatcher_hook generates valid dispatcher hook for global install."""
    installer = GitHooksInstaller(global_install=True)

    # Generate dispatcher for commit-msg
    dispatcher_content = installer._generate_dispatcher_hook("commit-msg", local=False)

    # Verify structure
    assert "#!/usr/bin/env python" in dispatcher_content, "Should have python shebang"
    assert "commit-msg" in dispatcher_content, "Should reference hook type"
    assert "subprocess.run" in dispatcher_content, "Should use subprocess.run"
    assert "*.hook" in dispatcher_content, "Should glob for .hook files"


def test_is_git_repository_valid(temp_git_repo: Path):
    """is_git_repository returns True for valid Git repository."""
    installer = GitHooksInstaller()
    assert installer.is_git_repository(temp_git_repo), "Should recognize valid Git repository"


def test_is_git_repository_invalid(tmp_path):
    """is_git_repository returns False for non-Git directory."""
    installer = GitHooksInstaller()

    # Create a directory without .git
    non_git_dir = tmp_path / "not-a-repo"
    non_git_dir.mkdir()

    assert not installer.is_git_repository(non_git_dir), "Should return False for non-Git directory"


def test_install_local_hooks_creates_dispatcher(temp_git_repo: Path):
    """install_local_hooks installs dispatcher hooks to .git/hooks directory."""
    installer = GitHooksInstaller(repo_path=str(temp_git_repo))
    success = installer.install_local_hooks()
    assert success, "Installation should succeed"
    hooks_dir = temp_git_repo / ".git" / "hooks"
    expected_hooks = ["pre-commit", "commit-msg"]
    for hook_name in expected_hooks:
        hook_file = hooks_dir / hook_name
        assert hook_file.exists(), f"Hook {hook_name} should be installed"
        content = hook_file.read_text()
        # Check for python shebang (python, not python3 for Windows compatibility)
        assert "#!/usr/bin/env python" in content, f"{hook_name} should have python shebang"
        assert "subprocess.run" in content, f"{hook_name} should use subprocess.run"


def test_install_local_hooks_fails_for_non_git_repo(tmp_path):
    """install_local_hooks returns False for non-Git directory."""
    # Create non-Git directory
    non_git_dir = tmp_path / "not-a-repo"
    non_git_dir.mkdir()

    installer = GitHooksInstaller(repo_path=str(non_git_dir))

    # Installation should fail
    success = installer.install_local_hooks()

    assert not success, "Installation should fail for non-Git repository"


def test_check_command_exists():
    """check_command_exists detects available commands."""
    installer = GitHooksInstaller()

    # Python should always exist (we're running in it)
    assert installer.check_command_exists("python") or installer.check_command_exists("python3"), "Python should be detected"

    # Git should exist (required by hooks)
    assert installer.check_command_exists("git"), "Git should be detected"

    # Non-existent command should return False
    assert not installer.check_command_exists("definitely-not-a-real-command-xyz123"), "Fake command should not be detected"


def test_check_prerequisites():
    """check_prerequisites validates Python and Git versions."""
    installer = GitHooksInstaller()

    # Prerequisites should pass (we're running the test)
    result = installer.check_prerequisites()

    assert result is True, "Prerequisites should be met"


def test_get_version_valid_command():
    """get_version returns version string for valid command."""
    installer = GitHooksInstaller()

    # Git should return version
    git_version = installer.get_version(["git", "--version"])
    assert git_version is not None, "Should return Git version"
    assert "git" in git_version.lower(), "Version string should contain 'git'"


def test_get_version_invalid_command():
    """get_version returns None for invalid command."""
    installer = GitHooksInstaller()

    # Fake command should return None
    version = installer.get_version(["definitely-not-a-real-command-xyz123", "--version"])
    assert version is None, "Should return None for invalid command"


def test_print_methods_dont_crash(capsys):
    """Print methods execute without errors."""
    installer = GitHooksInstaller()

    # Test all print methods
    installer.print_header("Test Header")
    installer.print_step("Test Step")
    installer.print_success("Test Success")
    installer.print_info("Test Info")
    installer.print_warning("Test Warning")
    installer.print_error("Test Error")

    # Verify something was printed
    captured = capsys.readouterr()
    assert len(captured.out) > 0, "Should print output"
    assert "Test Header" in captured.out, "Should print header"


def test_install_local_hooks_with_force_flag(temp_git_repo):
    """install_local_hooks with force=True overwrites existing hooks."""
    installer = GitHooksInstaller(repo_path=str(temp_git_repo))

    # Install first time
    installer.install_local_hooks()

    hooks_dir = temp_git_repo / ".git" / "hooks"
    pre_commit = hooks_dir / "pre-commit"

    # Modify the hook
    original_content = pre_commit.read_text()
    pre_commit.write_text("# Modified hook")

    # Install again without force - should skip
    installer2 = GitHooksInstaller(repo_path=str(temp_git_repo), force=False)
    installer2.install_local_hooks()

    assert pre_commit.read_text() == "# Modified hook", "Should not overwrite without force"

    # Install with force - should overwrite
    installer3 = GitHooksInstaller(repo_path=str(temp_git_repo), force=True)
    installer3.install_local_hooks()

    new_content = pre_commit.read_text()
    assert "subprocess.run" in new_content, "Should overwrite with force=True"
    assert new_content != "# Modified hook", "Content should change with force"


def test_print_summary(capsys):
    """print_summary outputs installation summary."""
    installer = GitHooksInstaller()

    installer.print_summary()

    captured = capsys.readouterr()
    assert "Installation Complete" in captured.out, "Should print completion message"
    assert "Next steps" in captured.out, "Should print next steps"


def test_install_global_hooks(monkeypatch):
    """install_global_hooks creates global hooks directory (mocked)."""
    import tempfile

    # Create a temporary directory for global hooks
    with tempfile.TemporaryDirectory() as tmpdir:
        fake_global_dir = Path(tmpdir) / ".git-hooks"

        # Mock Path.home() to return temp directory
        monkeypatch.setattr(Path, "home", lambda: Path(tmpdir))

        # Mock subprocess.run to avoid changing real Git config
        mock_calls = []

        def mock_run(cmd, **kwargs):
            mock_calls.append(cmd)
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

        monkeypatch.setattr(subprocess, "run", mock_run)

        installer = GitHooksInstaller(global_install=True)
        result = installer.install_global_hooks()

        assert result is True, "Global installation should succeed"
        assert fake_global_dir.exists(), "Global hooks directory should be created"

        # Verify Git config was called
        assert any("git" in str(call) for call in mock_calls), "Should call git config"


def test_install_global_hooks_git_config_failure(monkeypatch, temp_git_repo):
    """install_global_hooks returns False when Git config fails."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock Path.home()
        monkeypatch.setattr(Path, "home", lambda: Path(tmpdir))

        # Mock subprocess.run to simulate git config failure
        def mock_run_fail(cmd, **kwargs):
            if "git" in cmd and "config" in cmd:
                raise subprocess.CalledProcessError(1, cmd, stderr="Git config failed")
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

        monkeypatch.setattr(subprocess, "run", mock_run_fail)

        installer = GitHooksInstaller(global_install=True)
        result = installer.install_global_hooks()

        assert result is False, "Should return False when git config fails"


def test_run_method_local_install(temp_git_repo):
    """run() method executes local installation workflow."""
    installer = GitHooksInstaller(repo_path=str(temp_git_repo), global_install=False)

    # Run installation
    exit_code = installer.run()

    assert exit_code == 0, "Should return 0 on success"

    # Verify hooks were installed
    hooks_dir = temp_git_repo / ".git" / "hooks"
    assert (hooks_dir / "pre-commit").exists(), "pre-commit hook should exist"


def test_run_method_global_install(monkeypatch):
    """run() method executes global installation workflow."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock Path.home()
        monkeypatch.setattr(Path, "home", lambda: Path(tmpdir))

        # Mock subprocess.run to avoid changing real Git config
        def mock_run(cmd, **kwargs):
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

        monkeypatch.setattr(subprocess, "run", mock_run)

        installer = GitHooksInstaller(global_install=True)
        exit_code = installer.run()

        assert exit_code == 0, "Should return 0 on success"
