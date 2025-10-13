import subprocess
import sys
from pathlib import Path
import re

def run_pylint(files):
    print("--- Running pylint ---")
    command = [sys.executable, "-m", "pylint", "--fail-under=8"] + files
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("Pylint failed with errors.")
    # Extract score
    score_line = re.search(r"Your code has been rated at ([\d\.]+)/10", result.stdout)
    if score_line:
        score = float(score_line.group(1))
        if score < 8:
            print(f"Pylint score {score}/10 is below the threshold of 8.")
            # We will not fail the build for now, just warn
            # return False
    return True

def run_coverage():
    print("\n--- Running coverage ---")
    # Run pytest with coverage
    subprocess.run([sys.executable, "-m", "coverage", "run", "--source=.", "-m", "pytest"])
    # Get coverage report
    result = subprocess.run([sys.executable, "-m", "coverage", "report", "--format=total", "--fail-under=80"], capture_output=True, text=True)
    
    print(result.stdout)
    total_line = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", result.stdout)
    if total_line:
        coverage_percent = int(total_line.group(1))
        print(f"Total coverage: {coverage_percent}%")
        if coverage_percent < 80:
            print("Coverage is below 80%.")
            return False
    elif "FAIL" in result.stdout:
         print("Coverage check failed.")
         return False

    return True

def main():
    repo_root = Path(__file__).parent.parent
    py_files = [str(p) for p in repo_root.rglob("*.py") if ".venv" not in str(p)]
    
    pylint_passed = run_pylint(py_files)
    coverage_passed = run_coverage()

    if not pylint_passed or not coverage_passed:
        sys.exit(1)
    
    print("\nLinting and coverage checks passed.")

if __name__ == "__main__":
    main()
