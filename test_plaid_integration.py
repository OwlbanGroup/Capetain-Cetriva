import unittest


from unittest.mock import patch, MagicMock
from plaid_integration import PlaidIntegration


class TestPlaidIntegration(unittest.TestCase):
    def setUp(self):
        with patch('plaid_integration.plaid_api.PlaidApi') as MockPlaidApi:
            self.mock_client = MockPlaidApi.return_value
            self.plaid = PlaidIntegration()

    def test_create_link_token(self):
        self.mock_client.link_token_create.return_value.to_dict.return_value = {"link_token": "test_link_token"}
        response = self.plaid.create_link_token("user123")
        self.assertIn("link_token", response)
        self.assertEqual(response["link_token"], "test_link_token")

    def test_exchange_public_token(self):
        self.mock_client.item_public_token_exchange.return_value.to_dict.return_value = {"access_token": "test_access_token"}
        response = self.plaid.exchange_public_token("public_token_abc")
        self.assertIn("access_token", response)
        self.assertEqual(response["access_token"], "test_access_token")

    def test_get_accounts(self):
        self.mock_client.auth_get.return_value.to_dict.return_value = {"accounts": []}
        response = self.plaid.get_accounts("access_token_abc")
        self.assertIn("accounts", response)
        self.assertEqual(response["accounts"], [])


if __name__ == "__main__":
    unittest.main()
