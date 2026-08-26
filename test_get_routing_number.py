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

    @patch('get_routing_number.load_cache')
    @patch('get_routing_number.save_cache')
    def test_local_lookup_success(self, mock_save_cache, mock_load_cache):
        # The module uses a local mock database instead of a live API call.
        mock_load_cache.return_value = {}
        routing = get_routing_number('New Bank')
        self.assertEqual(routing, '987654321')
        mock_save_cache.assert_called_once()

    @patch('get_routing_number.load_cache')
    @patch('get_routing_number.save_cache')
    def test_fail_bank_returns_none(self, mock_save_cache, mock_load_cache):
        mock_load_cache.return_value = {}
        routing = get_routing_number('Fail Bank')
        self.assertIsNone(routing)
        mock_save_cache.assert_not_called()

    @patch('get_routing_number.load_cache')
    @patch('get_routing_number.save_cache')
    def test_bad_json_bank_returns_none(self, mock_save_cache, mock_load_cache):
        mock_load_cache.return_value = {}
        routing = get_routing_number('Bad JSON Bank')
        self.assertIsNone(routing)
        mock_save_cache.assert_not_called()


if __name__ == "__main__":
    unittest.main()