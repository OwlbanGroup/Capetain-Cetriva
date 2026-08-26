import unittest
from unittest.mock import patch
from banking_utils import BankingUtils


class TestBankingUtils(unittest.TestCase):
    """Unit tests for BankingUtils class with enhanced coverage."""

    @patch('banking_utils.generate_account_number')
    @patch('banking_utils.is_valid_account_number')
    def test_generate_account(self, mock_is_valid, mock_generate):
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
                if length