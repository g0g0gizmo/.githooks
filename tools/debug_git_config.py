"""Debug script to understand git config issue."""
import subprocess
from pathlib import Path
import tempfile

# Create a temp git repo
with tempfile.TemporaryDirectory() as tmpdir:
    repo = Path(tmpdir)
    
    # Initialize git repo
    subprocess.run(['git', 'init'], cwd=repo, capture_output=True, check=True)
    subprocess.run(['git', 'config', 'user.email', 'test@test.com'], cwd=repo, check=True)
    subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=repo, check=True)
    
    # Write to local config
    print("Writing to local config...")
    result = subprocess.run(['git', 'config', '--local', 'hooks.runtime.bash', '/test/bash'], cwd=repo, capture_output=True, text=True, check=False)
    print(f"Write result: returncode={result.returncode}")
    
    # Read from local config (with flag)
    print("\nReading from local config with --local flag...")
    result = subprocess.run(['git', 'config', '--local', 'hooks.runtime.bash'], cwd=repo, capture_output=True, text=True, check=False)
    print(f"Read with --local: returncode={result.returncode}, value={repr(result.stdout.strip())}")
    
    # Read from local config (without flag)
    print("\nReading from config without flag...")
    result = subprocess.run(['git', 'config', 'hooks.runtime.bash'], cwd=repo, capture_output=True, text=True, check=False)
    print(f"Read without flag: returncode={result.returncode}, value={repr(result.stdout.strip())}")
    
    # Unset with --local flag
    print("\nUnsetting with --local flag...")
    result = subprocess.run(['git', 'config', '--local', '--unset', 'hooks.runtime.bash'], cwd=repo, capture_output=True, text=True, check=False)
    print(f"Unset result: returncode={result.returncode}")
    
    # Try to read again
    print("\nReading after unset...")
    result = subprocess.run(['git', 'config', 'hooks.runtime.bash'], cwd=repo, capture_output=True, text=True, check=False)
    print(f"Read after unset: returncode={result.returncode}, value={repr(result.stdout.strip())}")
