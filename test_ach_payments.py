import unittest
from unittest.mock import patch, MagicMock
from ach_payments import ACHPayments


class TestACHPayments(unittest.TestCase):
    def setUp(self):
        self.ach = ACHPayments()
        self.ach.api_key = "test_api_key"  # Set a test API key

    @patch("ach_payments.requests.post")
    def test_create_payment_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "status": "success",
            "transaction_id": "12345",
        }
        mock_post.return_value = mock_response

        response = self.ach.create_payment(
            "123456789", "987654321", 100.0, "Test payment"
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.get("status"), "success")
        self.assertIn("transaction_id", response)

    
    @patch("ach_payments.requests.post")
    def test_create_payment_failure(self, mock_post):
        mock_post.side_effect = Exception("API error")

        response = self.ach.create_payment(
            "123456789", "987654321", 100.0, "Test payment"
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.get("status"), "failure")
    
        
    def test_create_payment_invalid_amount(self):
        response = self.ach.create_payment(
            "123456789", "987654321", -10.0, "Test payment"
        )
        self.assertIsNone(response)

    def test_create_payment_missing_account_or_routing(self):
        response = self.ach.create_payment("", "987654321", 100.0, "Test payment")
        self.assertIsNone(response)
        response = self.ach.create_payment("123456789", "", 100.0, "Test payment")
        self.assertIsNone(response)

    @patch("ach_payments.requests.get")
    def test_get_payment_status_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"status": "completed"}
        mock_get.return_value = mock_response

        response = self.ach.get_payment_status("12345")
        self.assertIsNotNone(response)
        self.assertEqual(response.get("status"), "completed")

    @patch("ach_payments.requests.get")
    def test_get_payment_status_failure(self, mock_get):
        mock_get.side_effect = Exception("API error")

        response = self.ach.get_payment_status("12345")
        self.assertIsNotNone(response)
        self.assertEqual(response.get("status"), "failure")
    
    def test_get_payment_status_missing_transaction_id(self):
        response = self.ach.get_payment_status("")

        self.assertIsNone(response)



if __name__ == "__main__":
    unittest.main()
