#!/usr/bin/env python
"""Fix flake8 issues in test_revenue_disbursement_oscar.py."""

with open("test_revenue_disbursement_oscar.py", "r") as f:
    content = f.read()

# Fix 1: E131 - fix continuation line indentation (line 16)
content = content.replace(
    "        DEFAULT_ROUTING_NUMBER,\n",
    "    DEFAULT_ROUTING_NUMBER,\n",
)

# Fix 2: E402 - add noqa to imports before environ set
content = content.replace(
    'import unittest\n',
    'import unittest  # noqa: E402\n',
)
content = content.replace(
    'from unittest.mock import MagicMock\n',
    'from unittest.mock import MagicMock  # noqa: E402\n',
)
content = content.replace(
    'from oscar_compensation import (\n',
    'from oscar_compensation import (  # noqa: E402\n',
)

# Fix 3: W391 - remove trailing blank line
content = content.rstrip() + "\n"

with open("test_revenue_disbursement_oscar.py", "w") as f:
    f.write(content)

print("Fixed all flake8 issues")
