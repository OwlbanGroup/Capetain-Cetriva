"""Integration tests running the manual integration script."""

import unittest

from integration_test_script import integration_test


class TestIntegration(unittest.TestCase):
    """Ensure the integration script executes without raising."""

    def test_integration_script_runs(self):
        """The integration script should complete without exceptions."""
        try:
            integration_test()
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.fail(f"Integration test script raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
