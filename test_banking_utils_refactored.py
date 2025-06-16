import unittest
from unittest.mock import patch
from banking_utils import BankingUtils


class TestBankingUtils(unittest.TestCase):
    \"\"\"Unit tests for BankingUtils class with enhanced coverage and parameterized tests.\"\"\"

    @patch('banking_utils.generate_account_number')
    @patch('banking_utils.is_valid_account_number')
    def test_generate_account(self, mock_is_valid, mock_generate):
        \"\"\"Test generate_account with various lengths and validation results.\"\"\"
        test_cases = [
            (9, '123456789', True, '123456789'),
            (9, '123', False, None),
            (0, None, None, None),
            (-5, None, None, None),
            (1, '1', True, '1'),
            (20, '12345678901234567890', True, '12345678901234567890'),
        ]
        for length, gen_return, valid_return, expected in test_cases:
            with self.subTest(length=length, gen_return=gen_return, valid_return=valid_return):
                if gen_return is not None:
                    mock_generate.return_value = gen_return
                else:
                    mock_generate.side_effect = Exception("Invalid length")
                if valid_return is not None:
                    mock_is_valid.return_value = valid_return
                else:
                    mock_is_valid.side_effect = Exception("Validation error")

                if length <= 0:
                    # For invalid lengths, expect None without calling generate_account_number
                    account = BankingUtils.generate_account(length)
                    self.assertIsNone(account)
                else:
                    account = BankingUtils.generate_account(length)
                    self.assertEqual(account, expected)

                # Reset mocks for next iteration
                mock_generate.reset_mock(side_effect=True)
                mock_is_valid.reset_mock(side_effect=True)

    @patch('banking_utils.get_routing_number')
    def test_get_routing(self, mock_get_routing):
        \"\"\"Test get_routing success and exception cases.\"\"\"
        # Success case
        mock_get_routing.return_value = '987654321'
        routing = BankingUtils.get_routing('Test Bank')
        self.assertEqual(routing, '987654321')

        # Exception case
        mock_get_routing.side_effect = Exception('API failure')
        routing = BankingUtils.get_routing('Test Bank')
        self.assertIsNone(routing)

    @patch('banking_utils.validate_routing_number')
    def test_validate_routing(self, mock_validate):
        \"\"\"Test validate_routing success and exception cases.\"\"\"
        # Success case
        mock_validate.return_value = True
        result = BankingUtils.validate_routing('987654321')
        self.assertTrue(result)

        # Exception case
        mock_validate.side_effect = Exception('Validation error')
        result = BankingUtils.validate_routing('987654321')
        self.assertFalse(result)

    @patch.object(BankingUtils.ach_payments, 'create_payment')
    def test_create_ach_payment(self, mock_create_payment):
        \"\"\"Test create_ach_payment success and exception cases.\"\"\"
        # Success case
        mock_create_payment.return_value = {'status': 'success'}
        response = BankingUtils.create_ach_payment('123', '456', 100.0)
        self.assertEqual(response['status'], 'success')

        # Exception case
        mock_create_payment.side_effect = Exception('Payment error')
        response = BankingUtils.create_ach_payment('123', '456', 100.0)
        self.assertIsNone(response)

    @patch.object(BankingUtils.ach_payments, 'get_payment_status')
    def test_get_ach_payment_status(self, mock_get_status):
        \"\"\"Test get_ach_payment_status success and exception cases.\"\"\"
        # Success case
        mock_get_status.return_value = {'status': 'completed'}
        status = BankingUtils.get_ach_payment_status('TX123')
        self.assertEqual(status['status'], 'completed')

        # Exception case
        mock_get_status.side_effect = Exception('Status error')
        status = BankingUtils.get_ach_payment_status('TX123')
        self.assertIsNone(status)

    @patch.object(BankingUtils.plaid_integration, 'create_link_token')
    def test_create_plaid_link_token(self, mock_create_link_token):
        \"\"\"Test create_plaid_link_token success and exception cases.\"\"\"
        # Success case
        mock_create_link_token.return_value = {'link_token': 'token123'}
        response = BankingUtils.create_plaid_link_token('user123')
        self.assertEqual(response['link_token'], 'token123')

        # Exception case
        mock_create_link_token.side_effect = Exception('Token error')
        response = BankingUtils.create_plaid_link_token('user123')
        self.assertIsNone(response)

    @patch.object(BankingUtils.plaid_integration, 'exchange_public_token')
    def test_exchange_plaid_public_token(self, mock_exchange_token):
        \"\"\"Test exchange_plaid_public_token success and exception cases.\"\"\"
        # Success case
        mock_exchange_token.return_value = {'access_token': 'access123'}
        response = BankingUtils.exchange_plaid_public_token('public_token')
        self.assertEqual(response['access_token'], 'access123')

        # Exception case
        mock_exchange_token.side_effect = Exception('Exchange error')
        response = BankingUtils.exchange_plaid_public_token('public_token')
        self.assertIsNone(response)

    @patch.object(BankingUtils.plaid_integration, 'get_accounts')
    def test_get_plaid_accounts(self, mock_get_accounts):
        \"\"\"Test get_plaid_accounts success and exception cases.\"\"\"
        # Success case
        mock_get_accounts.return_value = {'accounts': []}
        response = BankingUtils.get_plaid_accounts('access_token')
        self.assertEqual(response['accounts'], [])

        # Exception case
        mock_get_accounts.side_effect = Exception('Accounts error')
        response = BankingUtils.get_plaid_accounts('access_token')
        self.assertIsNone(response)

    def test_logging_on_generate_account_failure(self):
        \"\"\"Test that generate_account logs error on exception.\"\"\"
        with patch('banking_utils.generate_account_number', side_effect=Exception('Error')):
            with self.assertLogs('banking_utils', level='ERROR') as cm:
                account = BankingUtils.generate_account(9)
                self.assertIsNone(account)
                self.assertTrue(any('Error generating account number' in message for message in cm.output))

    def test_logging_on_invalid_account_number(self):
        \"\"\"Test that generate_account logs error when validation fails.\"\"\"
        with patch('banking_utils.generate_account_number', return_value='123'):
            with patch('banking_utils.is_valid_account_number', return_value=False):
                with self.assertLogs('banking_utils', level='ERROR') as cm:
                    account = BankingUtils.generate_account(9)
                    self.assertIsNone(account)
                    self.assertTrue(any('failed validation' in message for message in cm.output))


if __name__ == '__main__':
    unittest.main()
