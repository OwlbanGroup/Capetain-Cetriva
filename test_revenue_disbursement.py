"""Tests for revenue_disbursement.py DisbursementBatch integration.

Mocks BankingUtils module to avoid torch import overhead.
"""
import os

os.environ["TESTING"] = "1"

import sys  # noqa: E402
import unittest  # noqa: E402
from unittest.mock import MagicMock  # noqa: E402,F401

# Mock banking_utils BEFORE importing revenue_disbursement to avoid torch
# Save the original module reference to restore later
_original_banking_utils = sys.modules.get("banking_utils")

banking_utils_mock = MagicMock()
banking_utils_mock.BankingUtils = MagicMock
sys.modules["banking_utils"] = banking_utils_mock

from revenue_disbursement import DisbursementBatch  # noqa: E402,F401
from revenue_disbursement import DisbursementRecord  # noqa: E402,F401

# Restore the real banking_utils module so other test files can patch its
# attributes correctly (e.g. test_banking_utils.py uses @patch decorators).
if _original_banking_utils is not None:
    sys.modules["banking_utils"] = _original_banking_utils


def make_batch():
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


class TestAllocateOscarCompensation(unittest.TestCase):
    """Tests for allocate_oscar_compensation()."""

    def setUp(self):
        self.batch = make_batch()

    def test_allocate_calls_process_compensation(self):
        result = self.batch.allocate_oscar_compensation(150_000_000, 22_500_000)
        self.assertIsNotNone(result)
        self.assertTrue(self.batch.banking_utils.spend_profits_for_oscar.called)

    def test_allocate_correct_amount(self):
        self.batch.allocate_oscar_compensation(150_000_000, 22_500_000)
        call_args = self.batch.banking_utils.spend_profits_for_oscar.call_args
        self.assertAlmostEqual(call_args.args[0], 5_100_000, places=2)

    def test_allocate_with_description(self):
        self.batch.allocate_oscar_compensation(
            150_000_000, 22_500_000, description="2024 Annual"
        )
        call_args = self.batch.banking_utils.spend_profits_for_oscar.call_args
        self.assertIn("2024 Annual", call_args.kwargs["description"])

    def test_allocate_with_period(self):
        self.batch.allocate_oscar_compensation(
            150_000_000, 22_500_000, period="Q1 2024"
        )
        call_args = self.batch.banking_utils.spend_profits_for_oscar.call_args
        self.assertIn("Q1 2024", call_args.kwargs["description"])


class TestDisburseToStakeholder(unittest.TestCase):
    """Tests for disburse_to_stakeholder()."""

    def setUp(self):
        self.batch = make_batch()

    def test_disburse_creates_ach_payment(self):
        record = self.batch.disburse_to_stakeholder("Alice", 100_000, "Test")
        self.assertIsNotNone(record)
        self.assertEqual(record.recipient, "Alice")
        self.assertEqual(record.amount, 100_000)
        self.assertTrue(self.batch.banking_utils.create_ach_payment.called)

    def test_disburse_completed_status(self):
        record = self.batch.disburse_to_stakeholder("Bob", 50_000, "Q1 alloc")
        self.assertEqual(record.status, "completed")

    def test_disburse_has_transaction_id(self):
        record = self.batch.disburse_to_stakeholder("Eve", 75_000, "Q2 alloc")
        self.assertEqual(record.transaction_id, "ach_txn_001")

    def test_disburse_null_account_returns_none(self):
        self.batch.banking_utils.generate_account.return_value = None
        record = self.batch.disburse_to_stakeholder("Fail", 10_000, "fails")
        self.assertIsNone(record)

    def test_disburse_ach_failure_failed_record(self):
        self.batch.banking_utils.create_ach_payment.return_value = None
        record = self.batch.disburse_to_stakeholder("Char", 25_000, "fails")
        self.assertIsNotNone(record)
        self.assertEqual(record.status, "failed")

    def test_disburse_records_in_history(self):
        self.batch.disburse_to_stakeholder("Dave", 10_000, "test")
        self.assertEqual(len(self.batch._disbursement_history), 1)

    def test_disburse_default_routing_number(self):
        self.batch.disburse_to_stakeholder("Eve", 30_000, "test")
        call_args = self.batch.banking_utils.create_ach_payment.call_args
        self.assertEqual(call_args.args[1], "021000021")


class TestAllocateAndDisburse(unittest.TestCase):
    """Tests for allocate_and_disburse()."""

    def setUp(self):
        self.batch = make_batch()

    def test_allocation_keys_match_percentages(self):
        results = self.batch.allocate_and_disburse(1_000_000, "alloc")
        self.assertEqual(
            set(results.keys()), set(self.batch.ALLOCATION_PERCENTAGES.keys())
        )

    def test_allocation_amounts(self):
        results = self.batch.allocate_and_disburse(1_000_000, "alloc")
        self.assertAlmostEqual(
            results["Alternative Assets"].amount, 600_000, places=2
        )
        self.assertAlmostEqual(
            results["Public Equities"].amount, 300_000, places=2
        )
        self.assertAlmostEqual(
            results["Digital Assets"].amount, 100_000, places=2
        )

    def test_allocation_creates_three_records(self):
        self.batch.allocate_and_disburse(1_000_000, "alloc")
        self.assertEqual(len(self.batch._disbursement_history), 3)

    def test_allocation_zero_returns_empty(self):
        self.assertEqual(self.batch.allocate_and_disburse(0, "alloc"), {})

    def test_allocation_negative_returns_empty(self):
        self.assertEqual(self.batch.allocate_and_disburse(-1_000, "alloc"), {})


class TestDisbursementHistory(unittest.TestCase):
    """Tests for get_disbursement_history()."""

    def setUp(self):
        self.batch = make_batch()
        self.batch.disburse_to_stakeholder(
            "A", 10_000, "test A", asset_class="Alternative Assets"
        )
        self.batch.disburse_to_stakeholder(
            "B", 20_000, "test B", asset_class="Digital Assets"
        )

    def test_history_returns_all(self):
        self.assertEqual(len(self.batch.get_disbursement_history()), 2)

    def test_history_filter_by_recipient(self):
        history = self.batch.get_disbursement_history(recipient="A")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].recipient, "A")

    def test_history_filter_by_asset_class(self):
        history = self.batch.get_disbursement_history(asset_class="Digital Assets")
        self.assertEqual(len(history), 1)

    def test_history_filter_by_status(self):
        self.assertEqual(
            len(self.batch.get_disbursement_history(status="completed")), 2
        )


class TestDisbursementBatchProperties(unittest.TestCase):
    """Tests for DisbursementBatch.add_record, success_count, and failed_count."""

    def setUp(self):
        self.batch = make_batch()
        self.record1 = DisbursementRecord(
            recipient="Alice",
            account_number="111",
            routing_number="021000021",
            amount=5000,
            description="Payment 1",
            status="completed",
        )
        self.record2 = DisbursementRecord(
            recipient="Bob",
            account_number="222",
            routing_number="021000021",
            amount=7500,
            description="Payment 2",
            status="failed",
        )
        self.record3 = DisbursementRecord(
            recipient="Carol",
            account_number="333",
            routing_number="021000021",
            amount=2500,
            description="Payment 3",
            status="completed",
        )

    def test_add_record_updates_total(self):
        """add_record should append the record and update total_amount."""
        self.batch.add_record(self.record1)
        self.assertEqual(len(self.batch.records), 1)
        self.assertEqual(self.batch.total_amount, 5000)

        self.batch.add_record(self.record2)
        self.assertEqual(len(self.batch.records), 2)
        self.assertEqual(self.batch.total_amount, 12500)

    def test_success_count(self):
        self.batch.add_record(self.record1)
        self.batch.add_record(self.record2)
        self.batch.add_record(self.record3)
        self.assertEqual(self.batch.success_count, 2)

    def test_failed_count(self):
        self.batch.add_record(self.record1)
        self.batch.add_record(self.record2)
        self.batch.add_record(self.record3)
        self.assertEqual(self.batch.failed_count, 1)

class TestDisburseExceptionAndEdgeCases(unittest.TestCase):
    """Test exception handling and edge cases."""

    def test_disburse_exception_returns_none(self):
        """If BankingUtils raises, return None."""
        bu = MagicMock()
        bu.generate_account.return_value = "987654321"
        bu.create_ach_payment.side_effect = Exception("Gateway timeout")
        batch = DisbursementBatch(
            batch_id="BATCH-EXC",
            description="Exception batch",
            banking_utils=bu,
        )
        record = batch.disburse_to_stakeholder("Dave", 100_000, "Test")
        self.assertIsNone(record)
        self.assertFalse(batch._disbursement_history)

    def test_disburse_account_generation_fails(self):
        """When generate_account returns None, return None."""
        bu = MagicMock()
        bu.generate_account.return_value = None
        batch = DisbursementBatch(
            batch_id="BATCH-NO-ACCOUNT",
            description="No account batch",
            banking_utils=bu,
        )
        record = batch.disburse_to_stakeholder("Eve", 50_000, "Test")
        self.assertIsNone(record)
        self.assertFalse(batch.banking_utils.create_ach_payment.called)


class TestAllocateAndDisburseFailure(unittest.TestCase):
    """Test failure paths in allocate_and_disburse."""

    def test_allocation_when_disburse_returns_none(self):
        """If disburse_to_stakeholder fails, result is None for that key."""
        bu = MagicMock()
        bu.generate_account.return_value = None
        batch = DisbursementBatch(
            batch_id="BATCH-ALLOC-FAIL",
            description="Allocation failure",
            banking_utils=bu,
        )
        results = batch.allocate_and_disburse(1_000_000, "alloc")
        self.assertEqual(len(results), 3)
        for v in results.values():
            self.assertIsNone(v)


class TestDisbursementHistoryFilters(unittest.TestCase):
    """Additional tests for get_disbursement_history with date filters."""

    def setUp(self):
        from datetime import datetime
        self.batch = make_batch()
        self.record1 = DisbursementRecord(
            recipient="A",
            account_number="111",
            routing_number="021000021",
            amount=10000,
            description="test A",
            status="completed",
            asset_class="Alternative Assets",
            timestamp=datetime(2024, 1, 15),
        )
        self.record2 = DisbursementRecord(
            recipient="B",
            account_number="222",
            routing_number="021000021",
            amount=20000,
            description="test B",
            status="completed",
            asset_class="Digital Assets",
            timestamp=datetime(2024, 6, 20),
        )
        self.batch._disbursement_history = [self.record1, self.record2]

    def test_history_filter_by_start_date(self):
        from datetime import datetime
        history = self.batch.get_disbursement_history(
            start_date=datetime(2024, 3, 1)
        )
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].recipient, "B")

    def test_history_filter_by_end_date(self):
        from datetime import datetime
        history = self.batch.get_disbursement_history(
            end_date=datetime(2024, 3, 1)
        )
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].recipient, "A")

    def test_history_filter_no_match(self):
        history = self.batch.get_disbursement_history(recipient="NonExistent")
        self.assertEqual(history, [])


class TestEndToEndRevenueDisbursement(unittest.TestCase):
    """End-to-end: revenue allocation through Oscar compensation."""

    def test_e2e_oscar_compensation_payment(self):
        batch = make_batch()
        result = batch.allocate_oscar_compensation(150_000_000, 22_500_000)
        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["transaction_id"], "oscar_ach_002")
        call_args = batch.banking_utils.spend_profits_for_oscar.call_args
        self.assertAlmostEqual(call_args.args[0], 5_100_000, places=2)

    def test_e2e_combined_allocation(self):
        batch = make_batch()
        oscar_result = batch.allocate_oscar_compensation(150_000_000, 22_500_000)
        self.assertIsNotNone(oscar_result)
        results = batch.allocate_and_disburse(1_000_000, "Q2 allocation")
        self.assertEqual(len(results), 3)
        history = batch.get_disbursement_history()
        self.assertEqual(len(history), 3)


if __name__ == "__main__":
    unittest.main()
