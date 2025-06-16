import coverage
import unittest


def run_tests_with_coverage():
    cov = coverage.Coverage()
    cov.start()

    # Discover and run all tests
    loader = unittest.TestLoader()
    tests = loader.discover('.')
    testRunner = unittest.TextTestRunner(verbosity=2)
    _ = testRunner.run(tests)

    cov.stop()
    cov.save()

    print("\nCoverage Report:")
    cov.report(show_missing=True)

    # Optionally generate HTML report
    cov.html_report(directory='coverage_html_report')
    print(
        "HTML version of coverage report generated in coverage_html_report directory."
    )


if __name__ == "__main__":
    run_tests_with_coverage()
