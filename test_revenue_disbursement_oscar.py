"""Tests for Oscar Broome Compensation System integration.

Covers OscarCompensation-BankingUtils integration and revenue_disbursement
DisbursementBatch integration with OscarCompensation.
"""
import os

os.environ["TESTING"] = "1"

import unittest  # noqa: E402
from unittest.mock import MagicMock  # noqa: E402

from oscar_compensation import (  # noqa: E402
    OscarCompensation,
    OSCAR_OWNERSHIP_PERCENTAGE,
    DEFAULT_ROUTING_NUMBER,
)


def make_comp(banking_utils=None):
    """Create an OscarCompensation with mocked BankingUtils for tests."""
    if banking_utils is None:
        banking_utils = MagicMock()
        banking_utils.generate_account.return_value = "123456789"
        banking_utils.spend_profits_for_oscar.return_value = {
            "transaction_id": "test_txn_123",
            "status": "completed",
            "amount": 5100000.00,
        }
    return OscarCompensation(
        banking_utils=banking_utils,
        aum=150_000_000,
        ownership_pct=OSCAR_OWNERSHIP_PERCENTAGE,
        routing_number=DEFAULT_ROUTING_NUMBER,
    )


class TestIntegrationOscarCompensationBankingUtils(unittest.TestCase):
    """Integration tests for OscarCompensation and BankingUtils."""

    def setUp(self):
        self.comp = make_comp()

    def test_process_compensation_calls_spend_profits(self):
        """Verify process_compensation delegates to BankingUtils."""
        result = self.comp.process_compensation(150_000_000, 22_500_000)
        self.assertIsNotNone(result)
        self.assertTrue(self.comp.banking_utils.spend_profits_for_oscar.called)
        call_args = self.comp.banking_utils.spend_profits_for_oscar.call_args
        self.assertAlmostEqual(call_args.args[0], 5_100_000, places=2)

    def test_process_compensation_description_with_period(self):
        """Description includes period and compensation label."""
        self.comp.process_compensation(
            150_000_000, 22_500_000, description="Q2 2024 Report"
        )
        call_args = self.comp.banking_utils.spend_profits_for_oscar.call_args
        self.assertIn("Q2 2024 Report", call_args.kwargs["description"])
        self.assertIn("Oscar Broome Compensation", call_args.kwargs["description"])

    def test_process_compensation_no_description(self):
        """Description defaults to period-based label."""
        self.comp.process_compensation(
            150_000_000, 22_500_000, description="", period="Q1 2024"
        )
        call_args = self.comp.banking_utils.spend_profits_for_oscar.call_args
        self.assertIn("Oscar Broome Compensation", call_args.kwargs["description"])
        self.assertIn("Q1 2024", call_args.kwargs["description"])

    def test_process_compensation_payment_failure(self):
        """Payment failure returns None without raising."""
        self.comp.banking_utils.spend_profits_for_oscar.return_value = None
        result = self.comp.process_compensation(150_000_000, 22_500_000)
        self.assertIsNone(result)

    def test_full_flow_calculate_then_process(self):
        """Full flow: calculate compensation, then process payment."""
        breakdown = self.comp.calculate_compensation(
            150_000_000, 22_500_000, "2024 Annual"
        )
        self.assertEqual(breakdown.total_compensation, 5_100_000)
        result = self.comp.process_compensation(150_000_000, 22_500_000)
        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["transaction_id"], "test_txn_123")


class TestEndToEndCompensationWorkflow(unittest.TestCase):
    """End-to-end: AUM calculation flow through ACH payment."""

    def test_e2e_full_workflow(self):
        """Full workflow: calculate fees for realistic AUM and payment."""
        banking_utils = MagicMock()
        banking_utils.spend_profits_for_oscar.return_value = {
            "transaction_id": "e2e_txn",
            "status": "completed",
            "amount": 9800000.00,
        }
        comp = OscarCompensation(banking_utils=banking_utils, aum=350_000_000)
        aum = 350_000_000
        returns = aum * 0.12

        breakdown = comp.calculate_compensation(aum, returns, "2025 Annual")
        self.assertAlmostEqual(breakdown.gross_management_fee, 7_000_000, places=2)
        self.assertAlmostEqual(breakdown.gross_performance_fee, 2_800_000, places=2)
        self.assertAlmostEqual(breakdown.total_compensation, 9_800_000, places=2)

        result = comp.process_compensation(aum, returns)
        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "completed")
        call_args = banking_utils.spend_profits_for_oscar.call_args
        self.assertAlmostEqual(call_args.args[0], 9_800_000, places=2)
