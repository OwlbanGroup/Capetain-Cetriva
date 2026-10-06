"""Tests for Plaid integration."""

import unittest
from unittest.mock import MagicMock, patch

from plaid_integration import PlaidIntegration


class TestPlaidIntegration(unittest.TestCase):
    """Test cases for PlaidIntegration."""

    def setUp(self):
        self.plaid = PlaidIntegration()

    def test_create_link_token_success(self):
        mock_response = MagicMock()
        mock_response.to_dict.return_value = {"link_token": "test_token"}

        with patch.object(self.plaid.client, "link_token_create",
                          return_value=mock_response):
            response = self.plaid.create_link_token("user123")

        self.assertIsNotNone(response)
        self.assertIn("link_token", response)
        self.assertEqual(response["link_token"], "test_token")

    def test_create_link_token_failure(self):
        with patch.object(self.plaid.client, "link_token_create",
                          side_effect=Exception("API error")):
            response = self.plaid.create_link_token("user123")

        self.assertIsNone(response)

    def test_exchange_public_token_success(self):
        mock_response = MagicMock()
        mock_response.to_dict.return_value = {"access_token": "access123"}

        with patch.object(self.plaid.client, "item_public_token_exchange",
                          return_value=mock_response):
            response = self.plaid.exchange_public_token("public_token")

        self.assertIsNotNone(response)
        self.assertIn("access_token", response)
        self.assertEqual(response["access_token"], "access123")

    def test_exchange_public_token_failure(self):
        with patch.object(self.plaid.client, "item_public_token_exchange",
                          side_effect=Exception("API error")):
            response = self.plaid.exchange_public_token("public_token")

        self.assertIsNone(response)

    def test_get_accounts_success(self):
        mock_response = MagicMock()
        mock_response.to_dict.return_value = {"accounts": []}

        with patch.object(self.plaid.client, "auth_get",
                          return_value=mock_response):
            response = self.plaid.get_accounts("access_token")

        self.assertIsNotNone(response)
        self.assertIn("accounts", response)
        self.assertEqual(response["accounts"], [])

    def test_get_accounts_failure(self):
        with patch.object(self.plaid.client, "auth_get",
                          side_effect=Exception("API error")):
            response = self.plaid.get_accounts("access_token")

        self.assertIsNone(response)


if __name__ == "__main__":
    unittest.main()
