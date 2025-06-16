import unittest
from unittest.mock import patch
from get_routing_number import get_routing_number, load_cache, save_cache


class TestGetRoutingNumber(unittest.TestCase):
    def setUp(self):
        # Clear cache before each test
        self.cache = {}

    @patch('get_routing_number.load_cache')
    @patch('get_routing_number.save_cache')
    def test_cache_hit(self, mock_save_cache, mock_load_cache):
        mock_load_cache.return_value = {'test bank': {'routing_number': '123456789', 'timestamp': 1234567890}}
        routing = get_routing_number('Test Bank')
        self.assertEqual(routing, '123456789')
        mock_save_cache.assert_not_called()

    @patch('get_routing_number.requests.get')
    @patch('get_routing_number.load_cache')
    @patch('get_routing_number.save_cache')
    def test_api_call_success(self, mock_save_cache, mock_load_cache, mock_requests_get):
        mock_load_cache.return_value = {}
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'routingNumber': '987654321'}
        mock_requests_get.return_value = mock_response

        routing = get_routing_number('New Bank')
        self.assertEqual(routing, '987654321')
        mock_save_cache.assert_called_once()

    @patch('get_routing_number.requests.get')
    @patch('get_routing_number.load_cache')
    def test_api_call_failure(self, mock_load_cache, mock_requests_get):
        mock_load_cache.return_value = {}
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 500
        mock_requests_get.return_value = mock_response

        routing = get_routing_number('Fail Bank')
        self.assertIn('Failed to retrieve data', routing)

    @patch('get_routing_number.requests.get')
    @patch('get_routing_number.load_cache')
    def test_api_json_parse_error(self, mock_load_cache, mock_requests_get):
        mock_load_cache.return_value = {}
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("JSON decode error")
        mock_requests_get.return_value = mock_response

        routing = get_routing_number('Bad JSON Bank')
        self.assertIn('Failed to parse API response', routing)


if __name__ == "__main__":
    unittest.main()
