import os

NL = chr(10)
docstring = "Tests for test banking utils."
old_lines = [
    '"""',
    '',
    'import os',
    'os.environ.setdefault("TESTING", "1")',
    'os.environ.setdefault("PYTHONWARNINGS", "ignore")',
    '',
    '"' + docstring + '"""',
]
old = NL.join(old_lines)

with open("test_banking_utils.py", "rb") as f:
    content = f.read().decode("utf-8").replace(chr(13) + chr(10), chr(10))

print("old[:80]:", repr(old[:80]))
print("content[:80]:", repr(content[:80]))
print("old in content:", old in content)
for i in range(min(20, len(old), len(content))):
    if old[i] != content[i]:
        print(f"Mismatch at {i}: old={repr(old[i])} content={repr(content[i])}")
        break
else:
    print("First 20 chars match!")
