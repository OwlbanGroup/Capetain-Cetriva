import coverage
import unittest
import sys


def run_tests_with_coverage():
    cov = coverage.Coverage()
    cov.start()

    # Discover and run all tests
    loader = unittest.TestLoader()
    tests = loader.discover('.', pattern='test_*.py')
    testRunner = unittest.TextTestRunner(verbosity=2)
    result = testRunner.run(tests)

    cov.stop()
    cov.save()

    print("\nCoverage Report:")
    cov.report(show_missing=True)

    # Optionally generate HTML report
    cov.html_report(directory='coverage_html_report')
    print(
        "HTML version of coverage report generated in coverage_html_report directory."
    )

    # Exit with appropriate status code
    if not result.wasSuccessful():
        print("Some tests failed.")
        sys.exit(1)
    else:
        print("All tests passed successfully.")
        sys.exit(0)


if __name__ == "__main__":
    run_tests_with_coverage()
