import unittest


import time


from banking_utils import BankingUtils


class TestPerformanceAndEdgeCases(unittest.TestCase):

    def setUp(self):
        self.bank_utils = BankingUtils()

    def test_performance_account_generation(self):
        start_time = time.time()
        for _ in range(10000):
            account_number = self.bank_utils.generate_account(12)
            self.assertIsNotNone(account_number)
        duration = time.time() - start_time
        print(
            f"Account generation for 10,000 iterations took "
            f"{duration:.2f} seconds"
        )

    def test_performance_routing_retrieval(self):
        start_time = time.time()
        for _ in range(10000):
            routing_number = self.bank_utils.get_routing("Capetain Cetriva")
            self.assertIsNotNone(routing_number)
        duration = time.time() - start_time
        print(
            f"Routing retrieval for 10,000 iterations took "
            f"{duration:.2f} seconds"
        )

    def test_edge_case_empty_account_length(self):
        with self.assertRaises(ValueError):
            self.bank_utils.generate_account(0)

    def test_edge_case_negative_account_length(self):
        with self.assertRaises(ValueError):
            self.bank_utils.generate_account(-5)

    def test_edge_case_none_routing_number_validation(self):
        result = self.bank_utils.validate_routing(None)
        self.assertFalse(result)

    def test_edge_case_non_string_routing_number_validation(self):
        result = self.bank_utils.validate_routing(123456789)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
