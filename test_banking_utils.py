import unittest


from unittest.mock import patch
from banking_utils import BankingUtils


class TestBankingUtils(unittest.TestCase):

    @patch('banking_utils.generate_account_number')
    def test_generate_account(self, mock_generate_account_number):
        mock_generate_account_number.return_value = '123456789'
        result = BankingUtils.generate_account(9)
        self.assertEqual(result, '123456789')

    @patch('banking_utils.get_routing_number')
    def test_get_routing(self, mock_get_routing_number):
        mock_get_routing_number.return_value = '987654321'
        result = BankingUtils.get_routing('Capetain Cetriva')
        self.assertEqual(result, '987654321')

    @patch('banking_utils.validate_routing_number')
    def test_validate_routing(self, mock_validate_routing_number):
        mock_validate_routing_number.return_value = True
        result = BankingUtils.validate_routing('987654321')
        self.assertTrue(result)

    @patch('banking_utils.generate_account_number')
    def test_generate_account_exception(self, mock_generate_account_number):
        mock_generate_account_number.side_effect = Exception('Error')
        result = BankingUtils.generate_account(9)
        self.assertIsNone(result)

    @patch('banking_utils.get_routing_number')
    def test_get_routing_exception(self, mock_get_routing_number):
        mock_get_routing_number.side_effect = Exception('Error')
        result = BankingUtils.get_routing('Capetain Cetriva')
        self.assertIsNone(result)

    @patch('banking_utils.validate_routing_number')
    def test_validate_routing_exception(self, mock_validate_routing_number):
        mock_validate_routing_number.side_effect = Exception('Error')
        result = BankingUtils.validate_routing('987654321')
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
