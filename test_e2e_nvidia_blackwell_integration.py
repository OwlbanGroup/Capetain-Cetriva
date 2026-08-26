"""Unit tests for the E2E NVIDIA Blackwell integration orchestrator.

All external interactions (GPU library, market data downloads, ACH gateway)
are mocked so these tests run anywhere without hardware or network.
"""

# pylint: disable=protected-access  # unit tests target private helpers directly

import contextlib
import io
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

import e2e_nvidia_blackwell_integration as e2e


class TestInitializeSystem(unittest.TestCase):
    """Tests for E2ENVIDIAIntegration.initialize_system."""

    def _integrator(self, gpu_available=True, blackwell=True):
        integrator = e2e.E2ENVIDIAIntegration()
        integrator.nvidia = MagicMock()
        integrator.nvidia.get_gpu_info.return_value = {
            "gpu_available": gpu_available,
            "blackwell_compatible": blackwell,
        }
        return integrator

    def test_initialize_without_gpu_still_succeeds(self):
        """CPU fallback keeps the pipeline usable when no GPU exists."""
        integrator = self._integrator(gpu_available=False)
        self.assertTrue(integrator.initialize_system())
        integrator.nvidia.log_project_status.assert_called_once()

    def test_initialize_with_non_blackwell_gpu_warns_but_succeeds(self):
        """An older GPU logs a compatibility warning but does not fail."""
        integrator = self._integrator(gpu_available=True, blackwell=False)
        self.assertTrue(integrator.initialize_system())

    def test_initialize_with_compatible_gpu_succeeds(self):
        integrator = self._integrator()
        self.assertTrue(integrator.initialize_system())


class TestRunMarketAnalysis(unittest.TestCase):
    """Tests for E2ENVIDIAIntegration.run_market_analysis."""

    def setUp(self):
        self.integrator = e2e.E2ENVIDIAIntegration()
        self.integrator.nvidia = MagicMock()

    @patch("e2e_nvidia_blackwell_integration.MarketTrendAnalysis")
    def test_successful_prediction(self, mock_analysis_cls):
        instance = mock_analysis_cls.return_value
        frame = pd.DataFrame({"Close": [1.0, 2.0], "Target": [1, 1]})
        instance.download_data.return_value = frame
        instance.feature_engineering.return_value = frame
        instance.train_model.return_value = MagicMock()
        instance.data = frame

        result = self.integrator.run_market_analysis(ticker="NVDA")

        self.assertNotIn("error", result)
        self.assertEqual(result["ticker"], "NVDA")
        self.assertEqual(result["prediction"], "Positive")
        self.assertEqual(result["data_points"], 2)
        self.assertTrue(result["model_trained"])

    @patch("e2e_nvidia_blackwell_integration.MarketTrendAnalysis")
    def test_download_failure_returns_error(self, mock_analysis_cls):
        instance = mock_analysis_cls.return_value
        instance.download_data.return_value = None

        result = self.integrator.run_market_analysis(ticker="NVDA")

        self.assertEqual(result, {"error": "No data available"})


class TestExecuteBankingOperations(unittest.TestCase):
    """Tests for E2ENVIDIAIntegration.execute_banking_operations."""

    def setUp(self):
        self.integrator = e2e.E2ENVIDIAIntegration()
        self.integrator.banking_utils = MagicMock()

    def test_missing_credentials_return_error(self):
        self.integrator.banking_utils.generate_account.return_value = None
        self.integrator.banking_utils.get_routing.return_value = "021000021"

        result = self.integrator.execute_banking_operations(100.0)

        self.assertEqual(result, {"error": "Banking setup failed"})

    def test_successful_allocation_passthrough(self):
        self.integrator.banking_utils.generate_account.return_value = "123456789"
        self.integrator.banking_utils.get_routing.return_value = "021000021"
        allocations = {"Alternative Assets": {"status": "success"}}
        self.integrator.banking_utils.allocate_and_spend_profits.return_value = (
            allocations
        )

        result = self.integrator.execute_banking_operations(500.0)

        self.assertEqual(result["account"], "123456789")
        self.assertEqual(result["routing"], "021000021")
        self.assertEqual(result["allocations"], allocations)
        self.assertEqual(result["total_profits"], 500.0)


class TestRunFullPipeline(unittest.TestCase):
    """Tests for E2ENVIDIAIntegration.run_full_pipeline."""

    def test_initialization_failure_short_circuits(self):
        integrator = e2e.E2ENVIDIAIntegration()
        integrator.nvidia = MagicMock()
        integrator.initialize_system = MagicMock(return_value=False)

        results = integrator.run_full_pipeline()

        self.assertEqual(results, {"error": "NVIDIA initialization failed"})
        integrator.initialize_system.assert_called_once()


class TestSummaryPrinters(unittest.TestCase):
    """Tests for the console summary helper functions."""

    def _capture(self, func, arg):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            func(arg)
        return buffer.getvalue()

    def test_market_summary_success(self):
        output = self._capture(
            e2e._print_market_summary,
            {"prediction": "Positive", "ticker": "NVDA", "training_time": 1.5},
        )
        self.assertIn("Positive trend for NVDA", output)
        self.assertIn("1.50s", output)

    def test_market_summary_error(self):
        output = self._capture(
            e2e._print_market_summary, {"error": "No data available"}
        )
        self.assertIn("Market Analysis failed", output)

    def test_banking_summary_mixed_results(self):
        banking = {
            "account": "1234567890",
            "total_profits": 100.0,
            "allocations": {
                "Alternative Assets": {"status": "success"},
                "Public Equities": None,
                "Digital Assets": {"status": "success"},
            },
        }
        output = self._capture(e2e._print_banking_summary, banking)
        self.assertIn("Account 1234****", output)
        # Amounts reflect allocation percentages even when the payment failed
        # (the check/cross marker communicates success).
        self.assertIn("Alternative Assets: $60.00", output)
        self.assertIn("Public Equities: $30.00", output)
        self.assertIn("Digital Assets: $10.00", output)
        self.assertIn("\u2717 Public Equities", output)

    def test_banking_summary_error(self):
        output = self._capture(
            e2e._print_banking_summary, {"error": "Banking setup failed"}
        )
        self.assertIn("Banking Operations failed", output)


if __name__ == "__main__":
    unittest.main()
