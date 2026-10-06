#!/usr/bin/env bash
# Fast test runner - runs tests in TESTING mode without torch
set -euo pipefail

echo "Running tests in TESTING mode - no torch required..."
TESTING=1 PYTHONWARNINGS=ignore ACH_API_KEY=test-ci-key `
    python -m pytest -q --no-header
