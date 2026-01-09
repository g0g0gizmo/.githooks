# Standardized output/logging helpers for Git hooks
import sys
from typing import Optional


def print_success(msg: str):
    """Print a success message to stdout."""
    print(f"[OK] {msg}")


def print_error(msg: str, exit_code: Optional[int] = None):
    """Print an error message to stderr. Optionally exit with the given code."""
    print(f"[ERROR] {msg}", file=sys.stderr)
    if exit_code is not None:
        sys.exit(exit_code)


def print_warning(msg: str):
    """Print a warning message to stderr."""
    print(f"[WARNING] {msg}", file=sys.stderr)


def print_info(msg: str):
    """Print an informational message to stdout."""
    print(f"[INFO] {msg}")
