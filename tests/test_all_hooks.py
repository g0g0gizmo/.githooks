import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).parent.parent
HOOK_TYPES = [
    'applypatch-msg', 'commit-msg', 'post-commit', 'post-receive', 'post-rewrite',
    'pre-auto-gc', 'pre-commit', 'pre-push', 'pre-rebase', 'pre-receive', 'prepare-commit-msg'
]

def run_git(cmd, cwd, **kwargs):
    return subprocess.run(['git'] + cmd, cwd=cwd, capture_output=True, text=True, **kwargs)

def install_hooks(repo_dir):
    hooks_path = Path(repo_dir) / '.git' / 'hooks'
    hooks_path.mkdir(parents=True, exist_ok=True)
    for hook_type in HOOK_TYPES:
        hook_dir = REPO_ROOT / hook_type
        if not hook_dir.exists():
            continue
        for file in hook_dir.iterdir():
            # Make sure we're not copying directories (like __pycache__)
            if file.is_file() and (file.name.endswith('.hook') or file.name == hook_type):
                shutil.copy(file, hooks_path / file.name)

    # Special: pre-commit dispatcher
    dispatcher_src = REPO_ROOT / 'pre-commit' / 'dispatcher.py'
    dispatcher_dst = hooks_path / 'pre-commit'
    if dispatcher_src.exists():
        shutil.copy(dispatcher_src, dispatcher_dst)
        # On Windows, we need a batch file to ensure python runs the script
        if os.name == 'nt':
            with open(f"{dispatcher_dst}.bat", "w") as f:
                f.write(f'@"{sys.executable}" "%~dp0pre-commit" %*')

def test_all_hooks():
    # Ensure venv and deps
    subprocess.run([sys.executable, str(REPO_ROOT / 'bootstrap.py')], check=True)
    tmpdir = tempfile.mkdtemp()
    try:
        run_git(['init'], tmpdir)
        run_git(['config', 'user.name', 'Test User'], tmpdir)
        run_git(['config', 'user.email', 'test@example.com'], tmpdir)
        with open(os.path.join(tmpdir, 'README.md'), 'w') as f:
            f.write('test')
        run_git(['add', 'README.md'], tmpdir)
        run_git(['commit', '-m', 'init'], tmpdir)
        install_hooks(tmpdir)
        results = {}
        # Simulate actions for each hook type
        # Only simulate those that can be triggered in a test repo
        # pre-commit
        with open(os.path.join(tmpdir, 'file.txt'), 'w') as f:
            f.write('pre-commit')
        run_git(['add', 'file.txt'], tmpdir)
        result = run_git(['commit', '-m', 'test: pre-commit'], tmpdir)
        results['pre-commit'] = result.returncode
        # commit-msg
        with open(os.path.join(tmpdir, 'file2.txt'), 'w') as f:
            f.write('commit-msg')
        run_git(['add', 'file2.txt'], tmpdir)
        result = run_git(['commit', '-m', 'ISSUE-0000: commit-msg'], tmpdir)
        results['commit-msg'] = result.returncode
        # prepare-commit-msg
        with open(os.path.join(tmpdir, 'file3.txt'), 'w') as f:
            f.write('prepare-commit-msg')
        run_git(['add', 'file3.txt'], tmpdir)
        result = run_git(['commit', '-m', 'ISSUE-0000: prepare-commit-msg'], tmpdir)
        results['prepare-commit-msg'] = result.returncode
        # pre-push (simulate by calling hook directly if present)
        pre_push = Path(tmpdir) / '.git' / 'hooks' / 'pre-push'
        if pre_push.exists():
            result = subprocess.run([sys.executable, str(pre_push)], cwd=tmpdir)
            results['pre-push'] = result.returncode
        # pre-rebase (simulate by calling hook directly if present)
        pre_rebase = Path(tmpdir) / '.git' / 'hooks' / 'pre-rebase'
        if pre_rebase.exists():
            result = subprocess.run([sys.executable, str(pre_rebase)], cwd=tmpdir)
            results['pre-rebase'] = result.returncode
        # Print summary
        print("\nHOOK TEST SUMMARY:")
        for hook, code in results.items():
            print(f"{hook}: {'PASS' if code == 0 else 'FAIL'} (exit {code})")
        # Fail test if any hook fails
        assert all(code == 0 for code in results.values())
    finally:
        # Retry rmtree on Windows due to potential file locks
        for i in range(3):
            try:
                shutil.rmtree(tmpdir)
                break
            except PermissionError:
                time.sleep(0.1)
        else:
            shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == '__main__':
    test_all_hooks()