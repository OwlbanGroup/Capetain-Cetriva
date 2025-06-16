import unittest
from validate_routing_number import validate_routing_number


class TestValidateRoutingNumber(unittest.TestCase):
    def test_valid_routing_number(self):
        valid_number = "021000021"  # Example valid routing number
        self.assertTrue(validate_routing_number(valid_number))

    def test_invalid_routing_number(self):
        invalid_number = "123456789"
        self.assertFalse(validate_routing_number(invalid_number))

    def test_wrong_length(self):
        short_number = "12345678"
        long_number = "1234567890"
        self.assertFalse(validate_routing_number(short_number))
        self.assertFalse(validate_routing_number(long_number))

    def test_non_digit_input(self):
        non_digit = "abcdefghi"
        self.assertFalse(validate_routing_number(non_digit))

    def test_non_string_input(self):
        self.assertFalse(validate_routing_number(123456789))


if __name__ == "__main__":
    unittest.main()
