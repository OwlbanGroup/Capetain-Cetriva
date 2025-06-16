import unittest
from unittest.mock import patch, MagicMock
from plaid_integration import PlaidIntegration

class TestPlaidIntegration(unittest.TestCase):
    def setUp(self):
        self.plaid = PlaidIntegration()

    @patch('plaid_integration.plaid_api.PlaidApi.link_token_create')
    def test_create_link_token_success(self, mock_link_token_create):
        mock_response = MagicMock()
        mock_response.to_dict.return_value = {'link_token': 'test_token'}
        mock_link_token_create.return_value = mock_response

        response = self.plaid.create_link_token('user123')
        self.assertIsNotNone(response)
        self.assertIn('link_token', response)
        self.assertEqual(response['link_token'], 'test_token')

    @patch('plaid_integration.plaid_api.PlaidApi.link_token_create')
    def test_create_link_token_failure(self, mock_link_token_create):
        mock_link_token_create.side_effect = Exception('API error')

        response = self.plaid.create_link_token('user123')
        self.assertIsNone(response)

    @patch('plaid_integration.plaid_api.PlaidApi.item_public_token_exchange')
    def test_exchange_public_token_success(self, mock_exchange):
        mock_response = MagicMock()
        mock_response.to_dict.return_value = {'access_token': 'access123'}
        mock_exchange.return_value = mock_response

        response = self.plaid.exchange_public_token('public_token')
        self.assertIsNotNone(response)
        self.assertIn('access_token', response)
        self.assertEqual(response['access_token'], 'access123')

    @patch('plaid_integration.plaid_api.PlaidApi.item_public_token_exchange')
    def test_exchange_public_token_failure(self, mock_exchange):
        mock_exchange.side_effect = Exception('API error')

        response = self.plaid.exchange_public_token('public_token')
        self.assertIsNone(response)

    @patch('plaid_integration.plaid_api.PlaidApi.auth_get')
    def test_get_accounts_success(self, mock_auth_get):
        mock_response = MagicMock()
        mock_response.to_dict.return_value = {'accounts': []}
        mock_auth_get.return_value = mock_response

        response = self.plaid.get_accounts('access_token')
        self.assertIsNotNone(response)
        self.assertIn('accounts', response)
        self.assertEqual(response['accounts'], [])

    @patch('plaid_integration.plaid_api.PlaidApi.auth_get')
    def test_get_accounts_failure(self, mock_auth_get):
        mock_auth_get.side_effect = Exception('API error')

        response = self.plaid.get_accounts('access_token')
        self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main()
