import unittest
from unittest.mock import patch
from banking_utils import BankingUtils


class TestBankingUtils(unittest.TestCase):
    @patch('banking_utils.generate_account_number')
    def test_generate_account_success(self, mock_generate):
        mock_generate.return_value = '123456789'
        account = BankingUtils.generate_account(9)
        self.assertEqual(account, '123456789')

    @patch('banking_utils.generate_account_number')
    def test_generate_account_failure(self, mock_generate):
        mock_generate.side_effect = Exception("Generation error")
        account = BankingUtils.generate_account(9)
        self.assertIsNone(account)

    @patch('banking_utils.get_routing_number')
    def test_get_routing_success(self, mock_get_routing):
        mock_get_routing.return_value = '987654321'
        routing = BankingUtils.get_routing('Test Bank')
        self.assertEqual(routing, '987654321')

    @patch('banking_utils.get_routing_number')
    def test_get_routing_failure(self, mock_get_routing):
        mock_get_routing.side_effect = Exception("Retrieval error")
        routing = BankingUtils.get_routing('Test Bank')
        self.assertIsNone(routing)

    @patch('banking_utils.validate_routing_number')
    def test_validate_routing_success(self, mock_validate):
        mock_validate.return_value = True
        result = BankingUtils.validate_routing('987654321')
        self.assertTrue(result)

    @patch('banking_utils.validate_routing_number')
    def test_validate_routing_failure(self, mock_validate):
        mock_validate.side_effect = Exception("Validation error")
        result = BankingUtils.validate_routing('987654321')
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
