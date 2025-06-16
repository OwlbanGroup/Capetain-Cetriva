import unittest


from ach_payments import ACHPayments


class TestACHPayments(unittest.TestCase):
    def setUp(self):
        self.ach = ACHPayments()

    def test_create_payment(self):
        response = self.ach.create_payment(
            "123456789", "987654321", 100.0, "Test payment"
        )
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["account_number"], "123456789")
        self.assertEqual(response["routing_number"], "987654321")
        self.assertEqual(response["amount"], 100.0)
        self.assertEqual(response["description"], "Test payment")
        self.assertIn("transaction_id", response)

    def test_get_payment_status(self):
        status = self.ach.get_payment_status("ACH1234567890")
        self.assertEqual(status["transaction_id"], "ACH1234567890")
        self.assertEqual(status["status"], "completed")


if __name__ == "__main__":
    unittest.main()
