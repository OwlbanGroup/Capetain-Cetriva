#!/usr/bin/env bash
# Full CI validation - lints, types, and tests
set -euo pipefail

echo "=== 1. isort check ==="
python -m isort --check-only .

echo "=== 2. flake8 ==="
python -m flake8

echo "=== 3. pylint ==="
python -m pylint --rcfile=.pylintrc *.py

echo "=== 4. mypy ==="
./scripts/check_types.sh

echo "=== 5. pytest TESTING mode ==="
TESTING=1 PYTHONWARNINGS=ignore ACH_API_KEY=test-ci-key `
    python -m pytest -q --no-header

echo "=== All checks passed ==="
