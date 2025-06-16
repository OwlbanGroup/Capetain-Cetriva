import unittest
from unittest.mock import patch
from banking_utils import BankingUtils


class TestBankingUtils(unittest.TestCase):

    @patch('banking_utils.generate_account_number')
    @patch('banking_utils.is_valid_account_number')
    def test_generate_account_success(self, mock_is_valid, mock_generate):
        mock_generate.return_value = '123456789'
        mock_is_valid.return_value = True
        account = BankingUtils.generate_account(9)
        self.assertEqual(account, '123456789')

    @patch('banking_utils.generate_account_number')
    @patch('banking_utils.is_valid_account_number')
    def test_generate_account_failure(self, mock_is_valid, mock_generate):
        mock_generate.return_value = '123'
        mock_is_valid.return_value = False
        account = BankingUtils.generate_account(9)
        self.assertIsNone(account)

    @patch('banking_utils.get_routing_number')
    def test_get_routing_success(self, mock_get_routing):
        mock_get_routing.return_value = '987654321'
        routing = BankingUtils.get_routing('Test Bank')
        self.assertEqual(routing, '987654321')

    @patch('banking_utils.get_routing_number')
    def test_get_routing_failure(self, mock_get_routing):
        mock_get_routing.side_effect = Exception('API failure')
        routing = BankingUtils.get_routing('Test Bank')
        self.assertIsNone(routing)

    @patch('banking_utils.validate_routing_number')
    def test_validate_routing_success(self, mock_validate):
        mock_validate.return_value = True
        result = BankingUtils.validate_routing('987654321')
        self.assertTrue(result)

    @patch('banking_utils.validate_routing_number')
    def test_validate_routing_failure(self, mock_validate):
        mock_validate.side_effect = Exception('Validation error')
        result = BankingUtils.validate_routing('987654321')
        self.assertFalse(result)

    @patch('ach_payments.ACHPayments.create_payment')
    def test_create_ach_payment_success(self, mock_create_payment):
        mock_create_payment.return_value = {'status': 'success'}
        response = BankingUtils.create_ach_payment('123', '456', 100.0)
        self.assertEqual(response['status'], 'success')

    @patch('ach_payments.ACHPayments.create_payment')
    def test_create_ach_payment_failure(self, mock_create_payment):
        mock_create_payment.side_effect = Exception('Payment error')
        response = BankingUtils.create_ach_payment('123', '456', 100.0)
        self.assertIsNone(response)

    @patch('ach_payments.ACHPayments.get_payment_status')
    def test_get_ach_payment_status_success(self, mock_get_status):
        mock_get_status.return_value = {'status': 'completed'}
        status = BankingUtils.get_ach_payment_status('TX123')
        self.assertEqual(status['status'], 'completed')

    @patch('ach_payments.ACHPayments.get_payment_status')
    def test_get_ach_payment_status_failure(self, mock_get_status):
        mock_get_status.side_effect = Exception('Status error')
        status = BankingUtils.get_ach_payment_status('TX123')
        self.assertIsNone(status)
        
    @patch.object(BankingUtils.plaid_integration, 'create_link_token')
    def test_create_plaid_link_token_success(self, mock_create_link_token):
        mock_create_link_token.return_value = {'link_token': 'token123'}
        response = BankingUtils.create_plaid_link_token('user123')
        self.assertEqual(response['link_token'], 'token123')

    @patch.object(BankingUtils.plaid_integration, 'create_link_token')
    def test_create_plaid_link_token_failure(self, mock_create_link_token):
        mock_create_link_token.side_effect = Exception('Token error')
        response = BankingUtils.create_plaid_link_token('user123')
        self.assertIsNone(response)

    @patch.object(BankingUtils.plaid_integration, 'exchange_public_token')
    def test_exchange_plaid_public_token_success(self, mock_exchange_token):
        mock_exchange_token.return_value = {'access_token': 'access123'}
        response = BankingUtils.exchange_plaid_public_token('public_token')
        self.assertEqual(response['access_token'], 'access123')

    @patch.object(BankingUtils.plaid_integration, 'exchange_public_token')
    def test_exchange_plaid_public_token_failure(self, mock_exchange_token):
        mock_exchange_token.side_effect = Exception('Exchange error')
        response = BankingUtils.exchange_plaid_public_token('public_token')
        self.assertIsNone(response)

    @patch.object(BankingUtils.plaid_integration, 'get_accounts')
    def test_get_plaid_accounts_success(self, mock_get_accounts):
        mock_get_accounts.return_value = {'accounts': []}
        response = BankingUtils.get_plaid_accounts('access_token')
        self.assertEqual(response['accounts'], [])

    @patch.object(BankingUtils.plaid_integration, 'get_accounts')
    def test_get_plaid_accounts_failure(self, mock_get_accounts):
        mock_get_accounts.side_effect = Exception('Accounts error')
        response = BankingUtils.get_plaid_accounts('access_token')
        self.assertIsNone(response)


if __name__ == '__main__':
    unittest.main()
