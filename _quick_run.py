import os
os.environ["TESTING"] = "1"
import unittest, io, logging
logging.disable(logging.CRITICAL)

# Run tests one module at a time in separate processes
import subprocess, sys, re

modules = [
    "test_oscar_compensation",
    "test_revenue_disbursement",
    "test_revenue_disbursement_oscar",
    "test_banking_utils",
    "test_banking_utils_allocate_profits",
    "test_banking_utils_edge_cases",
    "test_banking_utils_extended",
    "test_banking_utils_refactored",
]

total_run = 0
for mod_name in modules:
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", mod_name, "-v"],
        capture_output=True, text=True,
        env=dict(os.environ, TESTING="1", PYTHONWARNINGS="ignore")
    )
    output = proc.stdout + proc.stderr
    m = re.search(r"Ran (\d+)", output)
    run_count = int(m.group(1)) if m else 0
    ok = "OK" in output.split("\n")[-3:]
    total_run += run_count
    print(f"{mod_name}: {run_count} tests, {'OK' if ok else 'FAILED'}")

print(f"\nTOTAL: {total_run} tests")
