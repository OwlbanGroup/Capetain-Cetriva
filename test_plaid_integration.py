import unittest


from unittest.mock import patch
from plaid_integration import PlaidIntegration


class TestPlaidIntegration(unittest.TestCase):
    def setUp(self):
        self.plaid = PlaidIntegration()

    @patch("plaid_integration.Client.LinkToken.create")
    def test_create_link_token(self, mock_create):
        mock_create.return_value = {"link_token": "test_link_token"}
        response = self.plaid.create_link_token("user123")
        self.assertIn("link_token", response)
        self.assertEqual(response["link_token"], "test_link_token")

    @patch("plaid_integration.Client.Item.public_token.exchange")
    def test_exchange_public_token(self, mock_exchange):
        mock_exchange.return_value = {"access_token": "test_access_token"}
        response = self.plaid.exchange_public_token("public_token_abc")
        self.assertIn("access_token", response)
        self.assertEqual(response["access_token"], "test_access_token")

    @patch("plaid_integration.Client.Auth.get")
    def test_get_accounts(self, mock_get):
        mock_get.return_value = {"accounts": []}
        response = self.plaid.get_accounts("access_token_abc")
        self.assertIn("accounts", response)
        self.assertEqual(response["accounts"], [])


if __name__ == "__main__":
    unittest.main()
