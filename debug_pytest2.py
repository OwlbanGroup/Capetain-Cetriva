import os, sys

# Add a debug plugin to trace import order
class DebugPlugin:
    def pytest_load_initial_conftests(self, early_config, parser, args):
        print("LOAD INITIAL CONFTESTS - TESTING:", os.environ.get("TESTING"), file=sys.stderr)

    def pytest_collection_modifyitems(self, items):
        print("COLLECTION MODIFYITEMS - TESTING:", os.environ.get("TESTING"), file=sys.stderr)
        for item in items:
            if "ach_payments" in item.name:
                print(f"  Test: {item.nodeid}", file=sys.stderr)

import pytest
sys.exit(pytest.main(["--no-cov", "-x", "-v", "--tb=short", "test_banking_utils.py", "-p", "no:cacheprovider"], plugins=[DebugPlugin()]))
