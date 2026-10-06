import sys, os

original_import = __builtins__.__import__

def tracking_import(name, *args, **kwargs):
    result = original_import(name, *args, **kwargs)
    if hasattr(result, '__file__') and result.__file__:
        fname = str(result.__file__)
        if 'banking_utils' in fname:
            t = os.environ.get('TESTING')
            print(f"IMPORT: {name} -> {fname}, TESTING={t}", file=sys.stderr)
    return result

__builtins__.__import__ = tracking_import

import pytest
sys.exit(pytest.main(["--no-cov", "--co", "-q", "-x"]))
