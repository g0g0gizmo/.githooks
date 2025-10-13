"""
hook_utils.py: Utility functions for Python git hooks
 - Tool checking and optional installation
 - Colored output (if colorama available)
 - Argument/usage helpers
"""
import shutil
import subprocess
import sys
import os

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init()
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    GREEN = Fore.GREEN
    RESET = Style.RESET_ALL
except ImportError:
    RED = YELLOW = GREEN = RESET = ''

def print_error(msg):
    print(f"{RED}{msg}{RESET}", file=sys.stderr)

def print_warn(msg):
    print(f"{YELLOW}{msg}{RESET}", file=sys.stderr)

def print_info(msg):
    print(f"{GREEN}{msg}{RESET}")

def tool_exists(tool):
    return shutil.which(tool) is not None

def prompt_install(tool, install_cmds):
    print_warn(f"Required tool '{tool}' not found.")
    resp = input(f"Install '{tool}' now? [y/N]: ").strip().lower()
    if resp == 'y':
        for cmd in install_cmds:
            print_info(f"Running: {cmd}")
            try:
                subprocess.check_call(cmd, shell=True)
            except Exception as e:
                print_error(f"Failed to install {tool}: {e}")
                return False
        print_info(f"{tool} installed. Please re-run the hook.")
        sys.exit(1)
    else:
        print_warn(f"Skipping hook because '{tool}' is not installed.")
        sys.exit(0)

def ensure_tool(tool, install_cmds):
    if not tool_exists(tool):
        prompt_install(tool, install_cmds)
        return False
    return True

def usage_exit(msg, code=0):
    print_warn(msg)
    sys.exit(code)