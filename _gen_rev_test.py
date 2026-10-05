#!/usr/bin/env python
"""Generate test_revenue_disbursement.py with BankingUtils mock."""

HEADER = '''"""Tests for revenue_disbursement.py DisbursementBatch integration.

Mocks BankingUtils module to avoid torch import overhead.
"""
import os
os.environ["TESTING"] = "1"

import sys
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

# Mock banking_utils BEFORE importing revenue_disbursement to avoid torch
_mock_bu = MagicMock()
_mock_bu.BankingUtils = MagicMock
sys.modules["banking_utils"] = _mock_bu

from revenue_disbursement import DisbursementBatch, DisbursementRecord  # noqa: E402
from oscar_compensation import (  # noqa: E402
    OSCAR_OWNERSHIP_PERCENTAGE,
    DEFAULT_ROUTING_NUMBER,
)


def make_batch():
    """Create a DisbursementBatch with mocked BankingUtils."""
    bu = MagicMock()
    bu.generate_account.return_value = "987654321"
    bu.create_ach_payment.return_value = {"transaction_id": "ach_txn_001"}
    bu.spend_profits_for_oscar.return_value = {
        "transaction_id": "oscar_ach_002",
        "status": "completed",
        "amount": 5100000.00,
    }
    return DisbursementBatch(
        batch_id="BATCH-TEST",
        description="Test batch",
        banking_utils=bu,
    )

'''

with open("test_revenue_disbursement.py", "w") as f:
    f.write(HEADER)

print("Created test_revenue_disbursement.py header")
