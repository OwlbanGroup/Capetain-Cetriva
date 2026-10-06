import os, sys, subprocess

env = dict(os.environ)
env['TESTING'] = '1'
env['ACH_API_KEY'] = 'test-ci-key'
env['PYTHONWARNINGS'] = 'ignore'

# Check what's importing banking_utils early
script = '''
import sys, os, importlib

class ImportTracer:
    def __init__(self):
        self.original = sys.modules.copy()
    def find_spec(self, name, path, target=None):
        if name == "banking_utils":
            import traceback
            print("=== IMPORTING banking_utils ===", file=sys.stderr)
            print(f"TESTING during import: {os.environ.get('TESTING')}", file=sys.stderr)
            traceback.print_stack(file=sys.stderr)
        return None

sys.meta_path.insert(0, ImportTracer())

import pytest
sys.exit(pytest.main(["--no-cov", "--co", "-q", "-x"]))
'''

r = subprocess.run(
    [sys.executable, '-c', script],
    env=env,
    capture_output=True, text=True,
    cwd=os.getcwd()
)
# Print only the relevant lines
for line in r.stderr.split('\n'):
    if 'banking_utils' in line.lower() or 'TESTING' in line or '=== IMPORTING' in line:
        print(line)
