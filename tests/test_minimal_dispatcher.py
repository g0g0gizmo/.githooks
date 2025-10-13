import subprocess
import sys
from pathlib import Path

import shutil
import tempfile

def test_direct_dispatcher_invocation():
    orig_dispatcher = Path(__file__).parent.parent / 'pre-commit' / 'dispatcher.py'
    with tempfile.TemporaryDirectory() as tmpdir:
        dispatcher_py = Path(tmpdir) / 'dispatcher_test.py'
        shutil.copy(orig_dispatcher, dispatcher_py)
        result = subprocess.run([sys.executable, str(dispatcher_py)], capture_output=True, text=True)
        print('STDOUT:', result.stdout)
        print('STDERR:', result.stderr)
        assert result.returncode == 0 or result.returncode == 1