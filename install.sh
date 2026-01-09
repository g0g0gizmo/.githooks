#!/bin/bash
# ==============================================================================
# Git Hooks Installer - Bash Wrapper
# ==============================================================================
# This script is a simple wrapper that calls the Python install.py script
#
# Usage: ./install.sh [--repo-path PATH] [--global] [--force] [--skip-deps]
#
# Examples:
#   ./install.sh                           - Install in current directory
#   ./install.sh --repo-path /path/to/repo - Install in specific repository
#   ./install.sh --global                  - Install globally
#   ./install.sh --force                   - Force reinstall
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_PY="${SCRIPT_DIR}/install.py"

# Colors
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 is not installed or not in PATH${NC}"
    echo -e "${RED}Please install Python 3.9+ from https://python.org${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${BLUE}[INFO] Found Python: ${PYTHON_VERSION}${NC}"

# Check if install.py exists
if [ ! -f "$INSTALL_PY" ]; then
    echo -e "${RED}[ERROR] install.py not found at ${INSTALL_PY}${NC}"
    exit 1
fi

# Run the Python installer (pass all arguments through)
echo -e "${CYAN}Running: python3 '${INSTALL_PY}' $@${NC}"
echo ""

python3 "$INSTALL_PY" "$@"
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo -e "${RED}[ERROR] Installation failed with exit code ${EXIT_CODE}${NC}"
    exit $EXIT_CODE
fi

exit 0
