#!/usr/bin/env python
"""Append integration test classes to test_revenue_disbursement_oscar.py."""

PART_1 = '''

class TestIntegrationOscarCompensationBankingUtils(unittest.TestCase):
    """Integration tests for OscarCompensation and BankingUtils."""

    def setUp(self):
        self.comp = make_comp()

    def test_process_compensation_calls_spend_profits_for_oscar(self):
        """Verify process_compensation delegates to BankingUtils."""
        result = self.comp.process_compensation(150_000_000, 22_500_000)
        self.assertTrue(self.comp.banking_utils.spend_profits_for_oscar.called)
        call_args = self.comp.banking_utils.spend_profits_for_oscar.call_args
        self.assertAlmostEqual(call_args.args[0], 5_100_000, places=2)

    def test_process_compensation_uses_correct_description(self):
        """Description includes period and compensation label."""
        self.comp.process_compensation(
            150_000_000, 22_500_000, description="Q2 2024 Report"
        )
        call_args = self.comp.banking_utils.spend_profits_for_oscar.call_args
        self.assertIn("Q2 2024 Report", call_args.kwargs["description"])
        self.assertIn("Oscar Broome Compensation", call_args.kwargs["description"])

    def test_process_compensation_no_description(self):
        """Description defaults to period-based label."""
        self.comp.calculate_compensation(150_000_000, 22_500_000, "Q1 2024")
        self.comp.process_compensation(150_000_000, 22_500_000, description="")
        call_args = self.comp.banking_utils.spend_profits_for_oscar.call_args
        self.assertIn("Oscar Broome Compensation", call_args.kwargs["description"])
        self.assertIn("Q1 2024", call_args.kwargs["description"])

    def test_process_compensation_payment_failure_returns_none(self):
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

'''

with open("test_revenue_disbursement_oscar.py", "a") as f:
    f.write(PART_1)

print("Part 1 appended")
