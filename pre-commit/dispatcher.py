import sys
import os
import subprocess

def main():
    hook_dir = os.path.dirname(os.path.abspath(__file__))
    exit_code = 0
    for fname in sorted(os.listdir(hook_dir)):
        if fname == 'dispatcher.py' or not fname.endswith('.hook'):
            continue

        hook_path = os.path.join(hook_dir, fname)
        if os.path.isfile(hook_path):
            print(f"[dispatcher] Running {hook_path}...")
            result = subprocess.run(
                [sys.executable, hook_path], 
                capture_output=True, text=True
            )
            
            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                print(result.stderr.strip(), file=sys.stderr)

            if result.returncode != 0:
                # A hook failed. Exit immediately.
                sys.exit(result.returncode)
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()