#!/usr/bin/env python
"""Run integration tests and capture output."""
import unittest, io
from test_revenue_disbursement_oscar import (
    TestIntegrationOscarCompensationBankingUtils,
    TestEndToEndCompensationWorkflow,
)

stream = io.StringIO()
loader = unittest.TestLoader()
suite = unittest.TestSuite()
suite.addTests(loader.loadTestsFromTestCase(TestIntegrationOscarCompensationBankingUtils))
suite.addTests(loader.loadTestsFromTestCase(TestEndToEndCompensationWorkflow))
result = unittest.TextTestRunner(verbosity=2, stream=stream).run(suite)

output = stream.getvalue()
with open("_test_out.txt", "w") as f:
    f.write(output)
    f.write(f"\nTests: {result.testsRun}, Failures: {len(result.failures)}, Errors: {len(result.errors)}")
print(f"Done: {result.testsRun} tests, {len(result.failures)} failures, {len(result.errors)} errors")
