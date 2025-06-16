import unittest


from generate_account_number import generate_account_number, is_valid_account_number


class TestGenerateAccountNumber(unittest.TestCase):

    def test_generate_default_length(self):
        account_number = generate_account_number()
        self.assertEqual(len(account_number), 9)
        self.assertTrue(is_valid_account_number(account_number))

    def test_generate_custom_length(self):
        length = 12
        account_number = generate_account_number(length)
        self.assertEqual(len(account_number), length)
        self.assertTrue(is_valid_account_number(account_number))

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            generate_account_number(1)


if __name__ == "__main__":
    unittest.main()
