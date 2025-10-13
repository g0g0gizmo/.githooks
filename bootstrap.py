import os
import sys
import subprocess
import platform
from pathlib import Path

def venv_exists(venv_path):
    return Path(venv_path).exists() and (Path(venv_path) / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")).exists()

def in_venv():
    return sys.prefix != sys.base_prefix

def main():
    venv_path = ".venv"
    if not venv_exists(venv_path):
        print("[bootstrap] venv not found, creating...")
        repo_root = Path(__file__).parent
        if os.name == "nt":
            subprocess.check_call(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(repo_root / "setup-venv.ps1")])
        else:
            subprocess.check_call(["bash", str(repo_root / "setup-venv.sh")])
    if not in_venv():
        # Re-invoke inside venv
        py = Path(venv_path) / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")
        print(f"[bootstrap] Re-invoking inside venv: {py}")
        os.execv(str(py), [str(py)] + sys.argv)
    # Now in venv, continue with main logic
    print("[bootstrap] venv is ready and active.")

if __name__ == "__main__":
    main()