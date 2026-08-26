"""Unit tests for BankingUtils.generate_account using mocked dependencies."""

import unittest
from unittest.mock import patch

from banking_utils import BankingUtils


class TestBankingUtils(unittest.TestCase):
    """Unit tests for BankingUtils class with enhanced coverage."""

    @patch('banking_utils.generate_account_number')
    @patch('banking_utils.is_valid_account_number')
    def test_generate_account(self, mock_is_valid, mock_generate):
        """Exercise generate_account across valid and invalid inputs."""
        test_cases = [
            (9, '123456789', True, '123456789'),
            (9, '123', False, None),
            (0, None, None, None),
            (-5, None, None, None),
            (1, '1', True, '1'),
            (20, '12345678901234567890', True, '12345678901234567890'),
        ]
        for length, gen_return, valid_return, expected in test_cases:
            subtest_kwargs = {
                'length': length,
                'gen_return': gen_return,
                'valid_return': valid_return,
            }
            with self.subTest(**subtest_kwargs):
                # Reset mocks between sub-tests to avoid state leakage.
                mock_generate.reset_mock(return_value=True, side_effect=True)
                mock_is_valid.reset_mock(return_value=True, side_effect=True)

                if gen_return is not None:
                    mock_generate.return_value = gen_return
                else:
                    # Invalid lengths raise ValueError, which BankingUtils catches.
                    mock_generate.side_effect = ValueError("Invalid length")
                if valid_return is not None:
                    mock_is_valid.return_value = valid_return
                else:
                    mock_is_valid.side_effect = ValueError("Validation error")

                result = BankingUtils.generate_account(length)

                if expected is None:
                    # Either generation raised ValueError or validation failed.
                    self.assertIsNone(result)
                else:
                    self.assertEqual(result, expected)
                    mock_is_valid.assert_called_once_with(expected)


if __name__ == "__main__":
    unittest.main()
