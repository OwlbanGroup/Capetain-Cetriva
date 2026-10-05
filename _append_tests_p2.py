#!/usr/bin/env python
"""Fix the test to pass period parameter to process_compensation."""

with open("test_revenue_disbursement_oscar.py", "r") as f:
    content = f.read()

content = content.replace(
    'self.comp.process_compensation(150_000_000, 22_500_000, description="")',
    'self.comp.process_compensation(150_000_000, 22_500_000, description="", period="Q1 2024")'
)

with open("test_revenue_disbursement_oscar.py", "w") as f:
    f.write(content)

print("Fixed test: added period parameter")


PART_2 = '''
class TestIntegrationRevenueDisbursementOscar(unittest.TestCase):
    """Integration tests for DisbursementBatch and OscarCompensation."""

    def setUp(self):
        from revenue_disbursement import DisbursementBatch
        self.bu = MagicMock()
        self.bu.generate_account.return_value = "987654321"
        self.bu.create_ach_payment.return_value = {"transaction_id": "db_txn"}
        self.bu.spend_profits_for_oscar.return_value = {
            "transaction_id": "oscar_txn",
            "status": "completed",
            "amount": 5100000.00,
        }
        self.batch = DisbursementBatch(
            batch_id="BATCH-001",
            description="Test disbursement batch",
            banking_utils=self.bu,
        )

    def test_allocate_oscar_compensation_calls_process(self):
        result = self.batch.allocate_oscar_compensation(150_000_000, 22_500_000)
        self.assertIsNotNone(result)
        self.assertTrue(self.bu.spend_profits_for_oscar.called)

    def test_allocate_oscar_compensation_correct_amount(self):
        self.batch.allocate_oscar_compensation(150_000_000, 22_500_000)
        call_args = self.bu.spend_profits_for_oscar.call_args
        self.assertAlmostEqual(call_args.args[0], 5_100_000, places=2)

    def test_allocate_and_disburse_uses_allocation_percentages(self):
        results = self.batch.allocate_and_disburse(1_000_000, "Test allocation")
        self.assertEqual(len(results), 3)
        for asset_class in self.batch.ALLOCATION_PERCENTAGES:
            self.assertIn(asset_class, results)
            self.assertIsNotNone(results[asset_class])

    def test_allocation_percentages_sum_to_one(self):
        total = sum(self.batch.ALLOCATION_PERCENTAGES.values())
        self.assertAlmostEqual(total, 1.0, places=10)

    def test_disbursement_history_after_allocation(self):
        self.batch.allocate_and_disburse(1_000_000, "Test allocation")
        self.assertEqual(len(self.batch._disbursement_history), 3)

    def test_get_disbursement_history_all(self):
        self.batch.allocate_and_disburse(1_000_000, "Test allocation")
        history = self.batch.get_disbursement_history()
        self.assertEqual(len(history), 3)

    def test_get_disbursement_history_filtered_by_recipient(self):
        self.batch.allocate_and_disburse(1_000_000, "Test allocation")
        history = self.batch.get_disbursement_history(recipient="Alternative Assets Allocation")
        self.assertEqual(len(history), 1)


class TestEndToEndCompensationWorkflow(unittest.TestCase):
    """End-to-end: AUM calculation flow through ACH payment."""

    def test_e2e_full_workflow(self):
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

if __name__ == "__main__":
    unittest.main()

'''

with open("test_revenue_disbursement_oscar.py", "a") as f:
    f.write(PART_2)

print("Part 2 appended")
