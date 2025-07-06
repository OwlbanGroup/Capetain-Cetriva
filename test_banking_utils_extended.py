import unittest
from unittest.mock import patch, MagicMock
from banking_utils import BankingUtils

class TestBankingUtilsExtended(unittest.TestCase):
    @patch.object(BankingUtils, 'create_ach_payment')
    @patch.object(BankingUtils, 'generate_account')
    def test_spend_profits_for_oscar_with_provided_account(self, mock_generate_account, mock_create_ach_payment):
        # Test with provided account number
        mock_create_ach_payment.return_value = {'status': 'success'}
        account_number = '123456789'
        amount = 1000.0
        description = 'Profit spending test'
        response = BankingUtils.spend_profits_for_oscar(amount, description, account_number)
        mock_create_ach_payment.assert_called_once_with(account_number, '021000021', amount, description)
        self.assertEqual(response, {'status': 'success'})
        mock_generate_account.assert_not_called()

    @patch.object(BankingUtils, 'create_ach_payment')
    @patch.object(BankingUtils, 'generate_account')
    def test_spend_profits_for_oscar_without_provided_account(self, mock_generate_account, mock_create_ach_payment):
        # Test without provided account number, should generate one
        mock_generate_account.return_value = '987654321'
        mock_create_ach_payment.return_value = {'status': 'success'}
        amount = 2000.0
        description = 'Profit spending test no account'
        response = BankingUtils.spend_profits_for_oscar(amount, description)
        mock_generate_account.assert_called_once()
        mock_create_ach_payment.assert_called_once_with('987654321', '021000021', amount, description)
        self.assertEqual(response, {'status': 'success'})

    @patch.object(BankingUtils, 'generate_account')
    def test_spend_profits_for_oscar_account_generation_failure(self, mock_generate_account):
        # Test failure to generate account number
        mock_generate_account.return_value = None
        amount = 500.0
        description = 'Profit spending test failure'
        response = BankingUtils.spend_profits_for_oscar(amount, description)
        mock_generate_account.assert_called_once()
        self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main()
