#!/usr/bin/env python3
"""
Show a cross-platform error popup from the command line.
Usage: python popup_error.py "Error message" ["Title"]
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: popup_error.py 'Error message' ['Title']", file=sys.stderr)
        sys.exit(1)
    message = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else "Hook Error"
