import os, sys
print("TESTING at start:", os.environ.get("TESTING"), file=sys.stderr)

import pytest

class DebugPlugin:
    def pytest_collection_finish(self, session):
        print("TESTING at collection finish:", os.environ.get("TESTING"), file=sys.stderr)
        if "banking_utils" in sys.modules:
            from banking_utils import BankingUtils
            print("ach_payments type:", type(BankingUtils.ach_payments).__name__, file=sys.stderr)
        else:
            print("banking_utils not in sys.modules!", file=sys.stderr)

sys.exit(pytest.main(["--no-cov", "-x", "-v", "--tb=short", "test_banking_utils.py::TestBankingUtils::test_create_ach_payment_failure"], plugins=[DebugPlugin()]))
