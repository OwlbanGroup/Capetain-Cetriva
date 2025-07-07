import unittest

from unittest.mock import patch
from banking_utils import BankingUtils


class TestAllocateAndSpendProfits(unittest.TestCase):

    @patch.object(BankingUtils, 'create_ach_payment')
    @patch.object(BankingUtils, 'generate_account')
    def test_allocate_and_spend_profits_success(
        self, mock_generate_account, mock_create_ach_payment
    ):
        mock_generate_account.side_effect = [
            '111111111',
            '222222222',
            '333333333',
        ]
        mock_create_ach_payment.return_value = {'status': 'success'}

        total_amount = 10000.0
        description = (
            'Test profit allocation'
        )
        responses = BankingUtils.allocate_and_spend_profits(
            total_amount, description
        )

        self.assertEqual(len(responses), 3)
        self.assertIn('Alternative Assets', responses)
        self.assertIn('Public Equities', responses)
        self.assertIn('Digital Assets', responses)

        for key, response in responses.items():
            self.assertIsNotNone(response)
            self.assertEqual(response['status'], 'success')

        self.assertEqual(mock_generate_account.call_count, 3)
        self.assertEqual(mock_create_ach_payment.call_count, 3)
    
    @patch.object(BankingUtils, 'create_ach_payment')
    @patch.object(BankingUtils, 'generate_account')
    def test_allocate_and_spend_profits_account_generation_failure(
        self, mock_generate_account, mock_create_ach_payment
    ):
        # Simulate failure to generate account number for second allocation
        mock_generate_account.side_effect = [
            '111111111',
            None,
            '333333333',
        ]
        mock_create_ach_payment.return_value = {'status': 'success'}

        total_amount = 10000.0
        description = (
            'Test profit allocation with failure'
        )
        responses = BankingUtils.allocate_and_spend_profits(total_amount, description)

        self.assertEqual(len(responses), 3)
        self.assertIsNotNone(responses['Alternative Assets'])
        self.assertIsNone(responses['Public Equities'])
        self.assertIsNotNone(responses['Digital Assets'])

        self.assertEqual(mock_generate_account.call_count, 3)
        self.assertEqual(mock_create_ach_payment.call_count, 2)


if __name__ == '__main__':
    unittest.main()
