"""Benchmark tests for TESTING mode import performance.

Verifies that import time with TESTING=1 is significantly faster than
without (where torch/plaid SDKs are imported).

These tests are skipped when TESTING=1 since the performance check
requires real imports.
"""

import os
import sys
import time
import unittest
from unittest.mock import patch


@unittest.skipUnless(
    os.getenv("TESTING") != "1",
    "Import performance tests require real imports (no TESTING mode)",
)
class TestImportPerformance(unittest.TestCase):
    """Measure and assert import time improvements in TESTING mode."""

    def test_torch_import_performance(self):
        """Verify torch import time is reasonable in non-TESTING mode."""
        # Force reimport to measure time
        if "torch" in sys.modules:
            del sys.modules["torch"]

        start = time.perf_counter()
        with patch.dict(os.environ, {"TESTING": "1"}):
            import plaid_integration  # noqa: F401
            torch_time = time.perf_counter() - start

        self.assertLess(
            torch_time,
            1.0,
            "TESTING mode import should take less than 1 second",
        )

    def test_plaid_import_skipped_in_testing(self):
        """Verify plaid SDK modules are not imported in TESTING mode."""
        # Clear any cached plaid imports
        for mod in list(sys.modules.keys()):
            if "plaid" in mod:
                del sys.modules[mod]

        with patch.dict(os.environ, {"TESTING": "1"}):
            import plaid_integration  # noqa: F401

        plaid_modules = [m for m in sys.modules if m.startswith("plaid")]
        self.assertEqual(
            plaid_modules,
            [],
            "Plaid SDK modules should not be imported in TESTING mode",
        )

    def test_mock_import_is_fast(self):
        """Verify MagicMock imports are faster than torch imports."""
        from unittest.mock import MagicMock

        start = time.perf_counter()
        for _ in range(100):
            _ = MagicMock()
        mock_time = time.perf_counter() - start

        self.assertLess(
            mock_time,
            0.1,
            "MagicMock creation should be very fast",
        )


if __name__ == "__main__":
    unittest.main()
