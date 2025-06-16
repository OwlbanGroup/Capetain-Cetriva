import unittest


from validate_routing_number import validate_routing_number


class TestValidateRoutingNumber(unittest.TestCase):

    def test_valid_routing_number(self):
        self.assertTrue(validate_routing_number("021000021"))  # Valid routing number

    def test_invalid_routing_number_length(self):
        self.assertFalse(validate_routing_number("12345678"))  # Too short
        self.assertFalse(validate_routing_number("1234567890"))  # Too long

    def test_invalid_routing_number_characters(self):
        self.assertFalse(validate_routing_number("12345678a"))  # Contains non-digit

    def test_invalid_routing_number_checksum(self):
        self.assertFalse(validate_routing_number("123456789"))  # Invalid checksum

    def test_non_string_input(self):
        self.assertFalse(validate_routing_number(123456789))  # Non-string input


if __name__ == "__main__":
    unittest.main()
