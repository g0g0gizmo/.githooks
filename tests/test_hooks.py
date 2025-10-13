import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import time
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HOOKS_DIR = REPO_ROOT / 'pre-commit'
PREPARE_COMMIT_MSG_DIR = REPO_ROOT / 'prepare-commit-msg'

def run_git(cmd, cwd, **kwargs):
    return subprocess.run(['git'] + cmd, cwd=cwd, capture_output=True, text=True, **kwargs)

# Always invoke Python scripts with sys.executable for cross-platform compatibility
def install_hook(src, dst_name, repo_dir, python_wrapper=False):
    hooks_path = Path(repo_dir) / '.git' / 'hooks'
    hooks_path.mkdir(parents=True, exist_ok=True)
    dst = hooks_path / dst_name
    shutil.copy(src, dst)
    if python_wrapper:
        # Create a .bat wrapper for Windows to call the script with python
        bat_path = hooks_path / (dst_name + '.bat')
        with open(bat_path, 'w') as f:
            f.write(f'@echo off\n"{sys.executable}" "%~dp0{dst_name}" %*\n')

def install_hook(src, dst_name, repo_dir):
    hooks_path = Path(repo_dir) / '.git' / 'hooks'
    hooks_path.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, hooks_path / dst_name)

class TestGitHooks(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        run_git(['init'], self.tmpdir)
        run_git(['config', 'user.name', 'Test User'], self.tmpdir)
        run_git(['config', 'user.email', 'test@example.com'], self.tmpdir)
        with open(os.path.join(self.tmpdir, 'README.md'), 'w') as f:
            f.write('test')
        run_git(['add', 'README.md'], self.tmpdir)
        run_git(['commit', '-m', 'init'], self.tmpdir)

    def tearDown(self):
        # shutil.rmtree can fail on Windows with PermissionError
        # because of file locks held by git processes.
        # Retry with a small delay to allow the locks to be released.
        for i in range(3):
            try:
                shutil.rmtree(self.tmpdir)
                break
            except PermissionError:
                time.sleep(0.1)
        else:
            shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_prevent_commit_to_main_creates_branch(self):
        # Copy dispatcher and hook to temp dir
        hooks_path = Path(self.tmpdir) / '.git' / 'hooks'
        hooks_path.mkdir(parents=True, exist_ok=True)
        dispatcher = hooks_path / 'dispatcher.py'
        prevent_hook = hooks_path / 'prevent-commit-to-main-or-develop.hook'
        shutil.copy(HOOKS_DIR / 'dispatcher.py', dispatcher)
        shutil.copy(HOOKS_DIR / 'prevent-commit-to-main-or-develop.hook', prevent_hook)
        # Switch to main
        run_git(['checkout', 'main'], self.tmpdir)
        # Try to run the dispatcher (simulating pre-commit)
        with open(os.path.join(self.tmpdir, 'file.txt'), 'w') as f:
            f.write('block')
        run_git(['add', 'file.txt'], self.tmpdir)
        result = subprocess.run([sys.executable, str(dispatcher)], cwd=self.tmpdir, capture_output=True, text=True)
        # The dispatcher should exit with a non-zero code, blocking the commit.
        self.assertNotEqual(result.returncode, 0)
        # The hook should NOT create a branch, just suggest one.
        current_branch = run_git(['rev-parse', '--abbrev-ref', 'HEAD'], self.tmpdir).stdout.strip()
        self.assertEqual(current_branch, 'main')
        self.assertIn("WARNING: Direct commits to 'main' are not allowed.", result.stderr)
        self.assertIn("Example: git checkout -b", result.stderr)

    def test_jira_enforcement(self):
        hooks_path = Path(self.tmpdir) / '.git' / 'hooks'
        hooks_path.mkdir(parents=True, exist_ok=True)
        enforce_hook = hooks_path / 'enforce-jira-id-match-branch.hook'
        shutil.copy(PREPARE_COMMIT_MSG_DIR / 'enforce-jira-id-match-branch.hook', enforce_hook)
        # Create a JIRA branch
        run_git(['checkout', '-b', 'feature/ABC-1234-test'], self.tmpdir)
        # Good commit
        with open(os.path.join(self.tmpdir, 'good.txt'), 'w') as f:
            f.write('good')
        run_git(['add', 'good.txt'], self.tmpdir)
        # Simulate prepare-commit-msg hook
        msg_file = os.path.join(self.tmpdir, 'COMMIT_EDITMSG')
        with open(msg_file, 'w') as f:
            f.write('ABC-1234: good')
        result = subprocess.run([sys.executable, str(enforce_hook), msg_file], cwd=self.tmpdir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        # Bad commit (wrong JIRA)
        with open(msg_file, 'w') as f:
            f.write('XYZ-9999: bad')
        result = subprocess.run([sys.executable, str(enforce_hook), msg_file], cwd=self.tmpdir, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

    def test_issue_0000_allowed_on_non_jira_branch(self):
        hooks_path = Path(self.tmpdir) / '.git' / 'hooks'
        hooks_path.mkdir(parents=True, exist_ok=True)
        enforce_hook = hooks_path / 'enforce-jira-id-match-branch.hook'
        shutil.copy(PREPARE_COMMIT_MSG_DIR / 'enforce-jira-id-match-branch.hook', enforce_hook)
        run_git(['checkout', '-b', 'no-jira-branch'], self.tmpdir)
        msg_file = os.path.join(self.tmpdir, 'COMMIT_EDITMSG')
        with open(msg_file, 'w') as f:
            f.write('ISSUE-0000: allowed')
        result = subprocess.run([sys.executable, str(enforce_hook), msg_file], cwd=self.tmpdir, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        # Not allowed: JIRA ID on non-JIRA branch
        with open(msg_file, 'w') as f:
            f.write('ABC-1234: not allowed')
        result = subprocess.run([sys.executable, str(enforce_hook), msg_file], cwd=self.tmpdir, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

if __name__ == '__main__':
    unittest.main()