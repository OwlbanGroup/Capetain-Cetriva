#!/usr/bin/env bash
# Type checking with mypy
set -euo pipefail

echo "Running mypy type checks..."
python -m mypy `
    account_routing_demo.py banking_utils.py ach_payments.py `
    plaid_integration.py nvidia_integration.py `
    generate_account_number.py get_routing_number.py `
    validate_routing_number.py e2e_nvidia_blackwell_integration.py `
    revenue_disbursement.py oscar_compensation.py `
    run_all_tests.py `
    --follow-imports=skip

echo "Type checking complete."
