import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HOOK_TYPES = [
    'applypatch-msg', 'commit-msg', 'post-commit', 'post-receive', 'post-rewrite',
    'pre-auto-gc', 'pre-commit', 'pre-push', 'pre-rebase', 'pre-receive', 'prepare-commit-msg'
]

def run_python_hook(hook_path):
    try:
        result = subprocess.run([sys.executable, str(hook_path)], capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, '', str(e)

def main():
    results = {}
    for hook_type in HOOK_TYPES:
        hook_dir = REPO_ROOT / hook_type
        if not hook_dir.exists():
            continue
        for file in hook_dir.iterdir():
            if file.suffix == '.hook' or file.name == 'dispatcher.py':
                code, out, err = run_python_hook(file)
                results[file] = (code, out, err)
    print("\nHOOKS TEST SUMMARY (in .githooks repo):")
    for file, (code, out, err) in results.items():
        print(f"\n{file} => {'PASS' if code == 0 else 'FAIL'} (exit {code})")
        if out.strip():
            print(f"  STDOUT: {out.strip()}")
        if err.strip():
            print(f"  STDERR: {err.strip()}")
    # Fail if any hook fails
    assert all(code == 0 for code, _, _ in results.values())

if __name__ == '__main__':
    main()