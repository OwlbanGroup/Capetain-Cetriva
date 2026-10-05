#!/usr/bin/env python
"""Fix indentation issue in test file line 42."""

with open("test_revenue_disbursement_oscar.py", "r") as f:
    lines = f.readlines()

# Line 42 (index 41) has wrong indentation - should be 4 spaces not 8
if len(lines) > 41:
    lines[41] = "    def test_process_compensation_calls_spend_profits_for_oscar(self):\n"

with open("test_revenue_disbursement_oscar.py", "w") as f:
    f.writelines(lines)

print("Fixed indentation")

