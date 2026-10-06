# Fix corrupted docstrings in test files

files_to_fix = [
    ('test_banking_utils.py', 'Tests for test banking utils.'),
    ('test_banking_utils_refactored.py', 'Unit tests for BankingUtils.generate_account using mocked dependencies.'),
    ('test_banking_utils_edge_cases.py', 'Tests for test banking utils edge cases.'),
    ('test_banking_utils_allocate_profits.py', 'Tests for test banking utils allocate profits.'),
    ('test_banking_utils_extended.py', 'Tests for test banking utils extended.'),
]

NL = chr(10)  # newline character

for filename, docstring in files_to_fix:
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8').replace('\r\n', '\n')
    
    # Build the old pattern with actual newlines
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
    
    new_lines = [
        '"""' + docstring + '"""',
        '',
        'import os',
        'os.environ.setdefault("TESTING", "1")',
        'os.environ.setdefault("PYTHONWARNINGS", "ignore")',
        '',
    ]
    new = NL.join(new_lines)
    
    if old in content:
        content = content.replace(old, new, 1)
        with open(filename, 'w') as f:
            f.write(content)
        print(f'Fixed: {filename}')
    else:
        print(f'No match: {filename}')
