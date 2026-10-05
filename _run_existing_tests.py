#!/usr/bin/env python
"""Run existing 33 oscar_compensation tests and capture output."""
import unittest, io

stream = io.StringIO()
suite = unittest.TestLoader().loadTestsFromName("test_oscar_compensation")
result = unittest.TextTestRunner(verbosity=2, stream=stream).run(suite)

output = stream.getvalue()
with open("_test_out2.txt", "w") as f:
    f.write(output)
    f.write(f"\nTests: {result.testsRun}, Failures: {len(result.failures)}, Errors: {len(result.errors)}")
print(f"Done: {result.testsRun} tests, {len(result.failures)} failures, {len(result.errors)} errors")
