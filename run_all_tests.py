"""Discover and run the full test suite, exiting non-zero on failure."""

import sys
import unittest


def run_all_tests():
    """Discover test_*.py modules in this directory and run them verbosely."""
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == '__main__':
    run_all_tests()
