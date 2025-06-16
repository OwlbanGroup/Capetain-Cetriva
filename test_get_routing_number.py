import unittest
from unittest.mock import patch, MagicMock
from get_routing_number import get_routing_number

class TestGetRoutingNumber(unittest.TestCase):

    @patch('get_routing_number.requests.get')
    @patch('get_routing_number.load_cache')
    @patch('get_routing_number.save_cache')
    def test_get_routing_number_cache_hit(self, mock_save_cache, mock_load_cache, mock_requests_get):
        mock_load_cache.return_value = {'capetain cetriva': {'routing_number': '123456789', 'timestamp': 1234567890}}
        result = get_routing_number('Capetain Cetriva')
        self.assertEqual(result, '123456789')
        mock_requests_get.assert_not_called()
        mock_save_cache.assert_not_called()

    @patch('get_routing_number.requests.get')
    @patch('get_routing_number.load_cache')
    @patch('get_routing_number.save_cache')
    def test_get_routing_number_api_success(self, mock_save_cache, mock_load_cache, mock_requests_get):
        mock_load_cache.return_value = {}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'routingNumber': '987654321'}
        mock_requests_get.return_value = mock_response

        result = get_routing_number('Capetain Cetriva')
        self.assertEqual(result, '987654321')
        mock_save_cache.assert_called_once()

    @patch('get_routing_number.requests.get')
    @patch('get_routing_number.load_cache')
    def test_get_routing_number_api_failure(self, mock_load_cache, mock_requests_get):
        mock_load_cache.return_value = {}
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_requests_get.return_value = mock_response

        result = get_routing_number('Capetain Cetriva')
        self.assertIn('Failed to retrieve data', result)

    @patch('get_routing_number.requests.get')
    @patch('get_routing_number.load_cache')
    def test_get_routing_number_json_parse_error(self, mock_load_cache, mock_requests_get):
        mock_load_cache.return_value = {}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("JSON decode error")
        mock_requests_get.return_value = mock_response

        result = get_routing_number('Capetain Cetriva')
        self.assertIn('Failed to parse API response', result)


if __name__ == "__main__":
    unittest.main()
