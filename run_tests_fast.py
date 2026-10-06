"""Convenience runner for fast test execution in TESTING mode.

Sets TESTING=1, PYTHONWARNINGS=ignore, and runs pytest with
optimized timeout settings. Use this for local development
and quick CI feedback.

Usage:
    python run_tests_fast.py            # Run all tests
    python run_tests_fast.py -v         # Verbose output
    python run_tests_fast.py test_foo   # Run specific test
"""

import argparse
import os
import subprocess
import sys
import time


def main():
    """Run pytest with TESTING mode and optimized settings."""
    parser = argparse.ArgumentParser(
        description="Fast test runner with TESTING mode enabled"
    )
    parser.add_argument(
        "pytest_args",
        nargs="*",
        help="Additional pytest arguments (e.g., test names, -v)",
    )
    parser.add_argument(
        "--no-coverage",
        action="store_true",
        help="Skip coverage reporting (faster)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Timeout per test in seconds (default: 60)",
    )
    args = parser.parse_args()

    # Build the pytest command
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "--no-header",
        f"--timeout={args.timeout}",
    ]

    if not args.no_coverage:
        cmd.extend([
            "--cov=.",
            "--cov-report=term-missing",
        ])

    cmd.extend(args.pytest_args)

    # Set environment variables
    env = dict(os.environ)
    env["TESTING"] = "1"
    env["PYTHONWARNINGS"] = "ignore"
    env.setdefault("ACH_API_KEY", "test-ci-key")

    print(f"Running tests with TESTING=1, timeout={args.timeout}s")
    print(f"Command: {' '.join(cmd)}")
    print()

    start = time.perf_counter()
    result = subprocess.run(cmd, env=env, check=False)
    elapsed = time.perf_counter() - start

    print(f"\nTests completed in {elapsed:.1f}s")
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
