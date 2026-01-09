# Git config helpers for reading/writing config values
import subprocess
from typing import Dict, Optional


def get_git_config(key: str, default: Optional[str] = None, scope: str = "local") -> Optional[str]:
    args = ["git", "config"]
    if scope == "global":
        args.append("--global")
    args.extend(["--get", key])
    result = subprocess.run(args, capture_output=True, check=False, encoding="utf-8", errors="replace")
    if result.returncode == 0:
        return result.stdout.strip()
    return default


def set_git_config(key: str, value: str, scope: str = "global") -> bool:
    args = ["git", "config"]
    if scope == "global":
        args.append("--global")
    args.extend([key, value])
    result = subprocess.run(args, check=False)
    return result.returncode == 0


def get_all_git_configs(prefix: str) -> Dict[str, str]:
    args = ["git", "config", "--get-regexp", f"^{prefix}"]
    result = subprocess.run(args, capture_output=True, check=False, encoding="utf-8", errors="replace")
    configs = {}
    if result.returncode == 0:
        for line in result.stdout.strip().splitlines():
            if line:
                k, v = line.split(None, 1)
                configs[k] = v
    return configs
