#!/usr/bin/env python3
"""
Profile git hook execution performance.

Measures execution time for all .hook files to identify bottlenecks.
Run before and after optimizations to quantify improvements.

Usage:
    python tools/profile-hooks.py
    python tools/profile-hooks.py > .github/performance-baseline-20251211.txt
"""
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple


def profile_hook_type(hook_type: str, repo_path: Path) -> Dict[str, Dict[str, float]]:
    """Profile all .hook files in a hook type directory.

    Args:
        hook_type: Git hook type (pre-commit, commit-msg, etc.)
        repo_path: Repository root path

    Returns:
        Dictionary mapping hook filename to timing data
    """
    hooks_dir = repo_path / hook_type
    if not hooks_dir.exists():
        return {}

    timings = {}
    hook_files = sorted(hooks_dir.glob("*.hook"))

    for hook_file in hook_files:
        if hook_file.name == "dispatcher.hook":
            continue

        start = time.perf_counter()
        try:
            result = subprocess.run([sys.executable, str(hook_file)], capture_output=True, timeout=30)
            duration = (time.perf_counter() - start) * 1000  # ms

            timings[hook_file.name] = {"duration_ms": duration, "exit_code": result.returncode, "error": None}
        except subprocess.TimeoutExpired:
            duration = 30000  # 30 seconds timeout
            timings[hook_file.name] = {"duration_ms": duration, "exit_code": -1, "error": "TIMEOUT"}
        except Exception as e:
            duration = (time.perf_counter() - start) * 1000
            timings[hook_file.name] = {"duration_ms": duration, "exit_code": -1, "error": str(e)}

    return timings


def main():
    """Main profiling entry point."""
    repo_path = Path(__file__).parent.parent
    hook_types = ["pre-commit", "prepare-commit-msg", "commit-msg", "post-commit"]

    print("Git Hooks Performance Profile")
    print("=" * 70)
    print(f"Repository: {repo_path}")
    print(f"Python: {sys.executable}")
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    total_time = 0
    hook_count = 0

    for hook_type in hook_types:
        timings = profile_hook_type(hook_type, repo_path)
        if timings:
            print(f"\n{hook_type}:")
            for hook_name, data in sorted(timings.items(), key=lambda x: x[1]["duration_ms"], reverse=True):
                duration = data["duration_ms"]
                total_time += duration
                hook_count += 1

                if data["error"]:
                    status = "X"
                    error_msg = f" ({data['error']})"
                elif data["exit_code"] == 0:
                    status = "OK"
                    error_msg = ""
                else:
                    status = "FAIL"
                    error_msg = f" (exit {data['exit_code']})"

                print(f"  {status} {hook_name:45s} {duration:8.2f}ms{error_msg}")

    print(f"\n{'=' * 70}")
    print(f"Total hooks: {hook_count}")
    print(f"Total time: {total_time:.2f}ms ({total_time/1000:.2f}s)")
    print(f"Average per hook: {total_time/hook_count:.2f}ms" if hook_count > 0 else "")
    print("=" * 70)

    # Performance assessment
    if total_time > 5000:
        print("\n[!] SLOW: Commits will take >5 seconds. Consider disabling slow hooks.")
    elif total_time > 2000:
        print("\n[!] MODERATE: Commits will take 2-5 seconds. Some optimization recommended.")
    elif total_time > 1000:
        print("\n[OK] ACCEPTABLE: Commits will take 1-2 seconds.")
    else:
        print("\n[OK] FAST: Commits will take <1 second.")


if __name__ == "__main__":
    main()
