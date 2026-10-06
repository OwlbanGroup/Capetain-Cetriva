"""Tests for the TESTING environment variable guard.

Verifies that when TESTING=1 is set, heavy ML imports (torch, plaid, nvidia)
are replaced with MagicMock instances instead of being imported.
"""

import os
import sys
import unittest
from unittest.mock import MagicMock

# Set TESTING before any imports that might trigger torch
os.environ["TESTING"] = "1"


class TestTestingGuardBankingUtils(unittest.TestCase):
    """Verify banking_utils.py uses MagicMock when TESTING=1."""

    @classmethod
    def setUpClass(cls):
        """Import banking_utils fresh with TESTING=1."""
        from banking_utils import BankingUtils
        cls.BankingUtils = BankingUtils

    def test_market_trend_analysis_is_mock(self):
        """MarketTrendAnalysis should be MagicMock when TESTING=1."""
        from banking_utils import MarketTrendAnalysis
        self.assertIsInstance(MarketTrendAnalysis, MagicMock)

    def test_nvidia_integration_is_mock(self):
        """nvidia_integration should be MagicMock when TESTING=1."""
        from banking_utils import nvidia_integration
        self.assertIsInstance(nvidia_integration, MagicMock)

    def test_torch_not_imported(self):
        """torch should not be in sys.modules when TESTING=1."""
        self.assertNotIn("torch", sys.modules)

    def test_banking_class_instantiable(self):
        """BankingUtils class should be importable and usable."""
        self.assertIsNotNone(self.BankingUtils)


class TestTestingGuardE2E(unittest.TestCase):
    """Verify e2e_nvidia_blackwell_integration.py uses MagicMock when TESTING=1."""

    @classmethod
    def setUpClass(cls):
        """Import e2e module fresh with TESTING=1."""
        from e2e_nvidia_blackwell_integration import (MarketTrendAnalysis,
                                                      nvidia_integration)
        cls.nvidia_integration = nvidia_integration
        cls.MarketTrendAnalysis = MarketTrendAnalysis

    def test_nvidia_integration_is_mock(self):
        """nvidia_integration should be MagicMock when TESTING=1."""
        self.assertIsInstance(self.nvidia_integration, MagicMock)

    def test_market_trend_analysis_is_mock(self):
        """MarketTrendAnalysis should be MagicMock when TESTING=1."""
        self.assertIsInstance(self.MarketTrendAnalysis, MagicMock)


class TestTestingGuardPlaidIntegration(unittest.TestCase):
    """Verify plaid_integration.py uses MagicMock when TESTING=1."""

    @classmethod
    def setUpClass(cls):
        """Import plaid_integration fresh with TESTING=1."""
        import plaid_integration
        cls.plaid_integration = plaid_integration

    def test_products_is_mock(self):
        """Products should be MagicMock when TESTING=1."""
        self.assertIsInstance(self.plaid_integration.Products, MagicMock)

    def test_configuration_is_mock(self):
        """Configuration should be MagicMock when TESTING=1."""
        self.assertIsInstance(
            self.plaid_integration.Configuration, MagicMock
        )

    def test_plaid_api_is_mock(self):
        """plaid_api should be MagicMock when TESTING=1."""
        self.assertIsInstance(
            self.plaid_integration.plaid_api, MagicMock
        )

    def test_plaid_not_imported(self):
        """plaid package should not be imported when TESTING=1."""
        self.assertNotIn("plaid.api", sys.modules)
        self.assertNotIn("plaid.model", sys.modules)


class TestTestingGuardMarketTrendAnalysis(unittest.TestCase):
    """Verify ai_models/test_market_trend_analysis.py mock behavior."""

    @classmethod
    def setUpClass(cls):
        """Import market_trend_analysis test module with TESTING=1."""
        from ai_models.test_market_trend_analysis import MarketTrendAnalysis
        cls.MarketTrendAnalysis = MarketTrendAnalysis

    def test_market_trend_analysis_is_mock(self):
        """MarketTrendAnalysis should be MagicMock when TESTING=1."""
        self.assertIsInstance(self.MarketTrendAnalysis, MagicMock)


if __name__ == "__main__":
    unittest.main()
