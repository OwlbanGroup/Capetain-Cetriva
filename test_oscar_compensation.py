"""Tests for Oscar Broome compensation calculations and payment processing."""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from oscar_compensation import (
    OscarCompensation,
    CompensationBreakdown,
    MANAGEMENT_FEE_RATE,
    PERFORMANCE_FEE_RATE,
    HURDLE_RATE,
    OSCAR_OWNERSHIP_PERCENTAGE,
    DEFAULT_AUM,
    DEFAULT_ROUTING_NUMBER,
)


def make_comp(aum=DEFAULT_AUM, ownership_pct=OSCAR_OWNERSHIP_PERCENTAGE):
    """Create an OscarCompensation without triggering BankingUtils import."""
    comp = OscarCompensation.__new__(OscarCompensation)
    comp.banking_utils = MagicMock()
    comp.aum = aum
    comp.ownership_pct = ownership_pct
    comp.routing_number = DEFAULT_ROUTING_NUMBER
    comp.history = []
    return comp


class TestManagementFeeCalculation(unittest.TestCase):
    """Tests for the management fee calculation (2% of AUM)."""

    def setUp(self):
        self.comp = make_comp()

    def test_management_fee_basic(self):
        """2% of AUM should be returned."""
        fee = self.comp.calculate_management_fee(100_000_000)
        self.assertAlmostEqual(fee, 2_000_000.0)

    def test_management_fee_default_aum(self):
        """Management fee with default AUM."""
        fee = self.comp.calculate_management_fee(DEFAULT_AUM)
        expected = DEFAULT_AUM * MANAGEMENT_FEE_RATE
        self.assertAlmostEqual(fee, expected)

    def test_management_fee_zero_aum(self):
        """Zero AUM yields zero fee."""
        self.assertEqual(self.comp.calculate_management_fee(0), 0.0)

    def test_management_fee_negative_aum(self):
        """Negative AUM yields negative fee (edge case)."""
        self.assertAlmostEqual(self.comp.calculate_management_fee(-50_000), -1_000.0)


class TestPerformanceFeeCalculation(unittest.TestCase):
    """Tests for the performance fee calculation (20% above 8% hurdle)."""

    def setUp(self):
        self.comp = make_comp()
        self.aum = 100_000_000

    def test_performance_fee_below_hurdle(self):
        """No performance fee when returns <= hurdle."""
        hurdle = self.aum * HURDLE_RATE
        fee = self.comp.calculate_performance_fee(self.aum, hurdle)
        self.assertEqual(fee, 0.0)

    def test_performance_fee_at_hurdle(self):
        """No performance fee when returns exactly equal hurdle."""
        fee = self.comp.calculate_performance_fee(self.aum, self.aum * 0.08)
        self.assertEqual(fee, 0.0)

    def test_performance_fee_above_hurdle(self):
        """20% of returns above 8% hurdle should be returned."""
        fee = self.comp.calculate_performance_fee(self.aum, 15_000_000)
        self.assertAlmostEqual(fee, 1_400_000.0)

    def test_performance_fee_zero_returns(self):
        """Zero returns yield zero performance fee."""
        self.assertEqual(self.comp.calculate_performance_fee(self.aum, 0), 0.0)

    def test_performance_fee_negative_returns(self):
        """Negative returns yield zero performance fee."""
        self.assertEqual(self.comp.calculate_performance_fee(self.aum, -1_000_000), 0.0)

    def test_performance_fee_large_returns(self):
        """Large returns yield proportionally large performance fee."""
        fee = self.comp.calculate_performance_fee(self.aum, 30_000_000)
        self.assertAlmostEqual(fee, 4_400_000.0)


class TestCompensationCalculation(unittest.TestCase):
    """Tests for total compensation calculation combining both fees."""

    def setUp(self):
        self.comp = make_comp(aum=100_000_000)

    def test_total_compensation_with_performance(self):
        """Compensation includes both management and performance fees."""
        breakdown = self.comp.calculate_compensation(
            100_000_000, 10_000_000, "Q1 2024"
        )
        self.assertAlmostEqual(breakdown.gross_management_fee, 2_000_000.0)
        self.assertAlmostEqual(breakdown.gross_performance_fee, 400_000.0)
        self.assertAlmostEqual(breakdown.total_compensation, 2_400_000.0)

    def test_total_compensation_no_performance(self):
        """Compensation is just management fee when returns <= hurdle."""
        breakdown = self.comp.calculate_compensation(
            100_000_000, 5_000_000, "Q1 2024"
        )
        self.assertAlmostEqual(breakdown.gross_management_fee, 2_000_000.0)
        self.assertEqual(breakdown.gross_performance_fee, 0.0)
        self.assertAlmostEqual(breakdown.total_compensation, 2_000_000.0)

    def test_compensation_history_tracked(self):
        """Each calculation should be added to history."""
        self.comp.calculate_compensation(100_000_000, 10_000_000, "Q1 2024")
        self.comp.calculate_compensation(100_000_000, 15_000_000, "Q2 2024")
        history = self.comp.get_compensation_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].period, "Q1 2024")
        self.assertEqual(history[1].period, "Q2 2024")

    def test_ownership_percentage_applied(self):
        """Compensation should reflect ownership percentage."""
        comp = make_comp(aum=100_000_000, ownership_pct=0.5)
        breakdown = comp.calculate_compensation(100_000_000, 15_000_000, "annual")
        self.assertAlmostEqual(breakdown.gross_management_fee, 2_000_000.0)
        self.assertAlmostEqual(breakdown.gross_performance_fee, 1_400_000.0)
        self.assertAlmostEqual(breakdown.net_management_fee, 1_000_000.0)
        self.assertAlmostEqual(breakdown.net_performance_fee, 700_000.0)
        self.assertAlmostEqual(breakdown.total_compensation, 1_700_000.0)

    def test_timestamp_set(self):
        """Each breakdown should have a timestamp."""
        breakdown = self.comp.calculate_compensation(100_000_000, 10_000_000)
        self.assertIsInstance(breakdown.timestamp, datetime)


class TestProcessCompensation(unittest.TestCase):
    """Tests for the process_compensation payment method."""

    @patch.object(OscarCompensation, 'calculate_compensation')
    def test_process_compensation_with_mock(self, mock_calc):
        """process_compensation should calculate and trigger ACH payment."""
        mock_calc.return_value = CompensationBreakdown(
            period="annual",
            aum=100_000_000,
            gross_management_fee=2_000_000,
            gross_performance_fee=1_400_000,
            returns=15_000_000,
            oscar_ownership_pct=1.0,
            net_management_fee=2_000_000,
            net_performance_fee=1_400_000,
            total_compensation=3_400_000,
        )
        comp = make_comp()
        comp.banking_utils.spend_profits_for_oscar = MagicMock(
            return_value={"status": "success"}
        )
        response = comp.process_compensation(100_000_000, 15_000_000, "Annual Bonus")
        self.assertEqual(response["status"], "success")
        comp.banking_utils.spend_profits_for_oscar.assert_called_once()

    @patch.object(OscarCompensation, 'calculate_compensation')
    def test_process_compensation_no_description(self, mock_calc):
        """process_compensation should generate description without input."""
        mock_calc.return_value = CompensationBreakdown(
            period="annual",
            aum=100_000_000,
            gross_management_fee=2_000_000,
            gross_performance_fee=0,
            returns=8_000_000,
            oscar_ownership_pct=1.0,
            net_management_fee=2_000_000,
            net_performance_fee=0,
            total_compensation=2_000_000,
        )
        comp = make_comp()
        comp.banking_utils.spend_profits_for_oscar = MagicMock(
            return_value={"status": "success"}
        )
        response = comp.process_compensation(100_000_000, 12_000_000)
        self.assertEqual(response["status"], "success")
        call_args = comp.banking_utils.spend_profits_for_oscar.call_args
        self.assertIn("Oscar Broome Compensation",
                      call_args.kwargs.get("description", ""))

    @patch.object(OscarCompensation, 'calculate_compensation')
    def test_process_compensation_payment_failure(self, mock_calc):
        """process_compensation should handle ACH failure gracefully."""
        mock_calc.return_value = CompensationBreakdown(
            period="test",
            aum=100_000_000,
            gross_management_fee=2_000_000,
            gross_performance_fee=0,
            returns=5_000_000,
            oscar_ownership_pct=1.0,
            net_management_fee=2_000_000,
            net_performance_fee=0,
            total_compensation=2_000_000,
        )
        comp = make_comp()
        comp.banking_utils.spend_profits_for_oscar = MagicMock(return_value=None)
        response = comp.process_compensation(
            100_000_000, 5_000_000, account_number="987654321"
        )
        self.assertIsNone(response)

    @patch.object(OscarCompensation, 'calculate_compensation')
    def test_process_compensation_spend_profits_integration(self, mock_calc):
        """process_compensation should pass correct amount to spend_profits_for_oscar."""
        mock_calc.return_value = CompensationBreakdown(
            period="Q1 2024",
            aum=150_000_000,
            gross_management_fee=3_000_000,
            gross_performance_fee=500_000,
            returns=15_000_000,
            oscar_ownership_pct=1.0,
            net_management_fee=3_000_000,
            net_performance_fee=500_000,
            total_compensation=3_500_000,
        )
        comp = make_comp()
        comp.banking_utils.spend_profits_for_oscar = MagicMock(
            return_value={"transaction_id": "txn_456"}
        )
        response = comp.process_compensation(
            150_000_000, 15_000_000, "Q1 Payout", account_number="111222333"
        )
        self.assertEqual(response["transaction_id"], "txn_456")
        call_args = comp.banking_utils.spend_profits_for_oscar.call_args
        self.assertEqual(call_args.args[0], 3_500_000)
        self.assertEqual(call_args.kwargs.get("description", ""),
                         "Q1 Payout - Oscar Broome Compensation (Q1 2024)")
        self.assertEqual(call_args.kwargs.get("account_number", ""), "111222333")


class TestGetOrGenerateAccount(unittest.TestCase):
    """Tests for the _get_or_generate_account helper."""

    def test_provided_account(self):
        """Should return the provided account number."""
        comp = make_comp()
        result = comp._get_or_generate_account("999999999")
        self.assertEqual(result, "999999999")

    def test_generated_account(self):
        """Should generate an account when none provided."""
        comp = make_comp()
        comp.banking_utils.generate_account.return_value = "123456789"
        result = comp._get_or_generate_account(None)
        self.assertEqual(result, "123456789")

    def test_account_generation_failure(self):
        """Should raise ValueError when account generation fails."""
        comp = make_comp()
        comp.banking_utils.generate_account.return_value = None
        with self.assertRaises(ValueError):
            comp._get_or_generate_account(None)


class TestSummary(unittest.TestCase):
    """Tests for the summary method."""

    def test_empty_history(self):
        """Summary should handle empty history gracefully."""
        comp = make_comp()
        self.assertEqual(comp.summary(), "No compensation records found.")

    def test_summary_with_records(self):
        """Summary should display compensation records."""
        comp = make_comp(aum=100_000_000)
        comp.calculate_compensation(100_000_000, 15_000_000, "Q1 2024")
        comp.calculate_compensation(100_000_000, 20_000_000, "Q2 2024")
        result = comp.summary()
        self.assertIn("Q1 2024", result)
        self.assertIn("Q2 2024", result)
        self.assertIn("Total:", result)

    def test_summary_with_filter(self):
        """Summary should filter by period when provided."""
        comp = make_comp(aum=100_000_000)
        comp.calculate_compensation(100_000_000, 15_000_000, "Q1 2024")
        comp.calculate_compensation(100_000_000, 20_000_000, "Q2 2024")
        result = comp.summary("Q1 2024")
        self.assertIn("Q1 2024", result)
        self.assertNotIn("Q2 2024", result)


class TestCreateDefault(unittest.TestCase):
    """Tests for the create_default factory method."""

    @patch.dict('sys.modules', {'banking_utils': MagicMock()})
    def test_create_default_with_env(self):
        """create_default should read AUM from environment."""
        import os
        os.environ['DEFAULT_AUM'] = '200000000'
        try:
            comp = OscarCompensation.create_default()
            self.assertEqual(comp.aum, 200_000_000)
        finally:
            os.environ.pop('DEFAULT_AUM', None)

    @patch.dict('sys.modules', {'banking_utils': MagicMock()})
    def test_create_default_defaults(self):
        """create_default should use module defaults when env not set."""
        import os
        os.environ.pop('DEFAULT_AUM', None)
        os.environ.pop('OSCAR_OWNERSHIP_PCT', None)
        os.environ.pop('ROUTING_NUMBER', None)
        comp = OscarCompensation.create_default()
        self.assertEqual(comp.aum, DEFAULT_AUM)
        self.assertEqual(comp.ownership_pct, OSCAR_OWNERSHIP_PERCENTAGE)
        self.assertEqual(comp.routing_number, DEFAULT_ROUTING_NUMBER)


class TestConstants(unittest.TestCase):
    """Verify configuration constants match the investment thesis."""

    def test_management_fee_rate(self):
        self.assertEqual(MANAGEMENT_FEE_RATE, 0.02)

    def test_performance_fee_rate(self):
        self.assertEqual(PERFORMANCE_FEE_RATE, 0.20)

    def test_hurdle_rate(self):
        self.assertEqual(HURDLE_RATE, 0.08)

    def test_ownership_percentage(self):
        self.assertEqual(OSCAR_OWNERSHIP_PERCENTAGE, 1.00)

    def test_routing_number(self):
        self.assertEqual(DEFAULT_ROUTING_NUMBER, "021000021")

    def test_default_aum(self):
        self.assertEqual(DEFAULT_AUM, 150_000_000)


if __name__ == '__main__':
    unittest.main()
