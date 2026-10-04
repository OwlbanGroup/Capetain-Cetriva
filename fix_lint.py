"""Fix indentation and trailing whitespace in test file."""
import re

with open('test_oscar_compensation.py', 'r') as f:
    lines = f.readlines()

# Fix the indentation on the assertEqual line
for i, line in enumerate(lines):
    if 'self.assertEqual(call_args.kwargs.get' in line and 'description' in line:
        lines[i] = '        self.assertEqual(call_args.kwargs.get("description", ""),\n'

# Remove trailing whitespace on all lines
for i, line in enumerate(lines):
    lines[i] = line.rstrip() + '\n' if line.strip() else '\n'

with open('test_oscar_compensation.py', 'w') as f:
    f.writelines(lines)
print('Fixed')
