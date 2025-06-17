import unittest
from unittest.mock import patch
from banking_utils import BankingUtils


class TestBankingUtils(unittest.TestCase):
    @patch('banking_utils.generate_account_number')
    @patch('banking_utils.is_valid_account_number')
    def test_generate_account_valid(self, mock_is_valid, mock_generate):
        mock_generate.return_value = '123456789'
        mock_is_valid.return_value = True
        account = BankingUtils.generate_account(9)
        self.assertEqual(account, '123456789')

    @patch('banking_utils.generate_account_number')
    @patch('banking_utils.is_valid_account_number')
    def test_generate_account_invalid(self, mock_is_valid, mock_generate):
        mock_generate.return_value = '123'
        mock_is_valid.return_value = False
        account = BankingUtils.generate_account(3)
        self.assertIsNone(account)

    @patch('banking_utils.get_routing_number')
    def test_get_routing_success(self, mock_get_routing):
        mock_get_routing.return_value = '987654321'
        routing = BankingUtils.get_routing('Test Bank')
        self.assertEqual(routing, '987654321')

    @patch('banking_utils.get_routing_number')
    def test_get_routing_failure(self, mock_get_routing):
        mock_get_routing.side_effect = Exception('Error')
        routing = BankingUtils.get_routing('Test Bank')
        self.assertIsNone(routing)

    @patch('banking_utils.validate_routing_number')
    def test_validate_routing_true(self, mock_validate):
        mock_validate.return_value = True
        result = BankingUtils.validate_routing('123456789')
        self.assertTrue(result)

    @patch('banking_utils.validate_routing_number')
    def test_validate_routing_false(self, mock_validate):
        mock_validate.return_value = False
        result = BankingUtils.validate_routing('123456789')
        self.assertFalse(result)

    @patch('banking_utils.BankingUtils.ach_payments', create=True)
    def test_create_ach_payment_success(self, mock_ach_payments):
        mock_ach_payments.create_payment.return_value = {'status': 'success'}
        response = BankingUtils.create_ach_payment('123', '456', 100.0, 'desc')
        self.assertEqual(response, {'status': 'success'})

    @patch('banking_utils.BankingUtils.ach_payments', create=True)
    def test_create_ach_payment_failure(self, mock_ach_payments):
        mock_ach_payments.create_payment.side_effect = Exception('Error')
        response = BankingUtils.create_ach_payment('123', '456', 100.0, 'desc')
        self.assertIsNone(response)

    @patch('banking_utils.BankingUtils.ach_payments', create=True)
    def test_get_ach_payment_status_success(self, mock_ach_payments):
        mock_ach_payments.get_payment_status.return_value = 'completed'
        status = BankingUtils.get_ach_payment_status('tx123')
        self.assertEqual(status, 'completed')

    @patch('banking_utils.BankingUtils.ach_payments', create=True)
    def test_get_ach_payment_status_failure(self, mock_ach_payments):
        mock_ach_payments.get_payment_status.side_effect = Exception('Error')
        status = BankingUtils.get_ach_payment_status('tx123')
        self.assertIsNone(status)

    @patch('banking_utils.BankingUtils.plaid_integration', create=True)
    def test_create_plaid_link_token_success(self, mock_plaid):
        mock_plaid.create_link_token.return_value = {'link_token': 'token'}
        response = BankingUtils.create_plaid_link_token('user1')
        self.assertEqual(response, {'link_token': 'token'})

    @patch('banking_utils.BankingUtils.plaid_integration', create=True)
    def test_create_plaid_link_token_failure(self, mock_plaid):
        mock_plaid.create_link_token.side_effect = Exception('Error')
        response = BankingUtils.create_plaid_link_token('user1')
        self.assertIsNone(response)

    @patch('banking_utils.BankingUtils.plaid_integration', create=True)
    def test_exchange_plaid_public_token_success(self, mock_plaid):
        mock_plaid.exchange_public_token.return_value = {'access_token': 'token'}
        response = BankingUtils.exchange_plaid_public_token('public_token')
        self.assertEqual(response, {'access_token': 'token'})

    @patch('banking_utils.BankingUtils.plaid_integration', create=True)
    def test_exchange_plaid_public_token_failure(self, mock_plaid):
        mock_plaid.exchange_public_token.side_effect = Exception('Error')
        response = BankingUtils.exchange_plaid_public_token('public_token')
        self.assertIsNone(response)

    @patch('banking_utils.BankingUtils.plaid_integration', create=True)
    def test_get_plaid_accounts_success(self, mock_plaid):
        mock_plaid.get_accounts.return_value = {'accounts': []}
        response = BankingUtils.get_plaid_accounts('access_token')
        self.assertEqual(response, {'accounts': []})

    @patch('banking_utils.BankingUtils.plaid_integration', create=True)
    def test_get_plaid_accounts_failure(self, mock_plaid):
        mock_plaid.get_accounts.side_effect = Exception('Error')
        response = BankingUtils.get_plaid_accounts('access_token')
        self.assertIsNone(response)


if __name__ == '__main__':
    unittest.main()
