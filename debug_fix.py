filename = 'test_banking_utils.py'
with open(filename, 'rb') as f:
    content = f.read().decode('utf-8').replace('\r\n', '\n')

# Print the first 200 chars with repr
print("Content first 200:")
print(repr(content[:200]))

# The docstring we expect
docstring = 'Tests for test banking utils.'
old = '"\"\"\\n\\nimport os\\nos.environ.setdefault(\"TESTING\", \"1\")\\nos.environ.setdefault(\"PYTHONWARNINGS\", \"ignore\")\\n\\n\"' + docstring + '\"\"\"'

print("\nLooking for:")
print(repr(old[:100]))

# Check character by character
print("\nChecking content vs pattern:")
for i in range(min(50, len(old), len(content))):
    if old[i] != content[i]:
        print(f"  Mismatch at {i}: old={repr(old[i])} content={repr(content[i])}")
        break
else:
    print("  First 50 chars match!")
