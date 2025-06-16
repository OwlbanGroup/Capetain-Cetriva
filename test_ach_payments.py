import unittest
from unittest.mock import patch, MagicMock

from ach_payments import ACHPayments


class TestACHPayments(unittest.TestCase):
    def setUp(self):
        self.ach = ACHPayments()

    @patch('ach_payments.requests.post')
    def test_create_payment(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "account_number": "123456789",
            "routing_number": "987654321",
            "amount": 100.0,
            "description": "Test payment",
            "transaction_id": "TX123456"
        }
        mock_post.return_value = mock_response

        response = self.ach.create_payment(
            "123456789", "987654321", 100.0, "Test payment"
        )
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["account_number"], "123456789")
        self.assertEqual(response["routing_number"], "987654321")
        self.assertEqual(response["amount"], 100.0)
        self.assertEqual(response["description"], "Test payment")
        self.assertIn("transaction_id", response)

    @patch('ach_payments.requests.get')
    def test_get_payment_status(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "transaction_id": "ACH1234567890",
            "status": "completed"
        }
        mock_get.return_value = mock_response

        status = self.ach.get_payment_status("ACH1234567890")
        self.assertEqual(status["transaction_id"], "ACH1234567890")
        self.assertEqual(status["status"], "completed")


if __name__ == "__main__":
    unittest.main()
