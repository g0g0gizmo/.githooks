#!/bin/sh
# Wrapper to call Python dispatcher for pre-commit hooks
SCRIPT_DIR="$(dirname "$0")"
python3 "$SCRIPT_DIR/dispatcher.py"
exit $?