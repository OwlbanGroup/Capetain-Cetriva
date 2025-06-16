import unittest
from unittest.mock import patch
from banking_utils import BankingUtils

class TestBankingUtilsEdgeCases(unittest.TestCase):

    def test_generate_account_invalid_length_zero(self):
        account = BankingUtils.generate_account(0)
        self.assertIsNone(account)

    def test_generate_account_invalid_length_negative(self):
        account = BankingUtils.generate_account(-5)
        self.assertIsNone(account)

    @patch('banking_utils.get_routing_number')
    def test_get_routing_exception(self, mock_get_routing):
        mock_get_routing.side_effect = Exception("API failure")
        routing = BankingUtils.get_routing("Test Bank")
        self.assertIsNone(routing)

    @patch('banking_utils.validate_routing_number')
    def test_validate_routing_exception(self, mock_validate):
        mock_validate.side_effect = Exception("Validation error")
        result = BankingUtils.validate_routing("123456789")
        self.assertFalse(result)

    @patch.object(BankingUtils.ach_payments, 'create_payment')
    def test_create_ach_payment_exception(self, mock_create_payment):
        mock_create_payment.side_effect = Exception("Create payment error")
        response = BankingUtils.create_ach_payment("123", "456", 100.0)
        self.assertIsNone(response)

    @patch.object(BankingUtils.ach_payments, 'get_payment_status')
    def test_get_ach_payment_status_exception(self, mock_get_status):
        mock_get_status.side_effect = Exception("Get status error")
        status = BankingUtils.get_ach_payment_status("TX123")
        self.assertIsNone(status)

    @patch.object(BankingUtils.plaid_integration, 'create_link_token')
    def test_create_plaid_link_token_exception(self, mock_create_link_token):
        mock_create_link_token.side_effect = Exception("Create link token error")
        response = BankingUtils.create_plaid_link_token("user123")
        self.assertIsNone(response)

    @patch.object(BankingUtils.plaid_integration, 'exchange_public_token')
    def test_exchange_plaid_public_token_exception(self, mock_exchange_token):
        mock_exchange_token.side_effect = Exception("Exchange token error")
        response = BankingUtils.exchange_plaid_public_token("public_token")
        self.assertIsNone(response)

    @patch.object(BankingUtils.plaid_integration, 'get_accounts')
    def test_get_plaid_accounts_exception(self, mock_get_accounts):
        mock_get_accounts.side_effect = Exception("Get accounts error")
        response = BankingUtils.get_plaid_accounts("access_token")
        self.assertIsNone(response)

if __name__ == "__main__":
    unittest.main()
