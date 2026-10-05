#!/usr/bin/env python
"""Run coverage on oscar_compensation.py and capture output."""
import subprocess
import sys
import os

os.environ["TESTING"] = "1"

# Run coverage
proc = subprocess.run(
    [sys.executable, "-m", "coverage", "run", "--source=oscar_compensation",
     "-m", "unittest", "test_oscar_compensation"],
    capture_output=True, text=True
)
with open("_cov_test_out.txt", "w") as f:
    f.write(proc.stdout)
    f.write(proc.stderr)
    f.write(f"\nReturn code: {proc.returncode}")

# Run coverage report
proc2 = subprocess.run(
    [sys.executable, "-m", "coverage", "report", "--show-missing"],
    capture_output=True, text=True
)
with open("_cov_report.txt", "w") as f:
    f.write(proc2.stdout)
    f.write(proc2.stderr)
    f.write(f"\nReturn code: {proc2.returncode}")

print(f"Coverage run: {proc.returncode}")
print("Report in _cov_report.txt")
