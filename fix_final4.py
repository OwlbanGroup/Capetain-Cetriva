files_to_fix = [
    ('test_banking_utils.py', 'Tests for test banking utils.'),
    ('test_banking_utils_refactored.py', 'Unit tests for BankingUtils.generate_account using mocked dependencies.'),
    ('test_banking_utils_edge_cases.py', 'Tests for test banking utils edge cases.'),
    ('test_banking_utils_allocate_profits.py', 'Tests for test banking utils allocate profits.'),
    ('test_banking_utils_extended.py', 'Tests for test banking utils extended.'),
]

for filename, docstring in files_to_fix:
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8').replace('\r\n', '\n')
    
    old = '"""\n\nimport os\nos.environ.setdefault("TESTING", "1")\nos.environ.setdefault("PYTHONWARNINGS", "ignore")\n\n"' + docstring + '"""'
    new = '"""' + docstring + '"""\n\nimport os\nos.environ.setdefault("TESTING", "1")\nos.environ.setdefault("PYTHONWARNINGS", "ignore")\n'
    
    if old in content:
        content = content.replace(old, new, 1)
        with open(filename, 'w', newline='\n') as f:
            f.write(content)
        print(f'Fixed: {filename}')
    else:
        print(f'No match: {filename}')
        # Show what we're looking for
        print(f'  Looking for: {repr(old[:80])}...')
