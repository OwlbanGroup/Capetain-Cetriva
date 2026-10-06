# Fix all corrupted test files - the opening """ became ""

files_to_fix = [
    'test_banking_utils.py',
    'test_banking_utils_refactored.py',
    'test_banking_utils_edge_cases.py',
    'test_banking_utils_allocate_profits.py',
    'test_banking_utils_extended.py',
]

docstrings = {
    'test_banking_utils.py': 'Tests for test banking utils.',
    'test_banking_utils_refactored.py': 'Unit tests for BankingUtils.generate_account using mocked dependencies.',
    'test_banking_utils_edge_cases.py': 'Tests for test banking utils edge cases.',
    'test_banking_utils_allocate_profits.py': 'Tests for test banking utils allocate profits.',
    'test_banking_utils_extended.py': 'Tests for test banking utils extended.',
}

NL = chr(10)

for filename in files_to_fix:
    with open(filename, 'rb') as f:
        raw = f.read()
    
    content = raw.decode('utf-8')
    content = content.replace(chr(13) + chr(10), NL)
    
    docstring = docstrings[filename]
    
    # The corrupted pattern starts with "" instead of """
    # Pattern: ""\n\nimport os\nos.environ.setdefault("TESTING", "1")\nos.environ.setdefault("PYTHONWARNINGS", "ignore")\n\n"Tests for docstring."""
    
    corrupted = '""' + NL + NL + 'import os' + NL + 'os.environ.setdefault("TESTING", "1")' + NL + 'os.environ.setdefault("PYTHONWARNINGS", "ignore")' + NL + NL + '"' + docstring + '"""'
    fixed = '"""' + docstring + '"""' + NL + NL + 'import os' + NL + 'os.environ.setdefault("TESTING", "1")' + NL + 'os.environ.setdefault("PYTHONWARNINGS", "ignore")' + NL
    
    if corrupted in content:
        content = content.replace(corrupted, fixed, 1)
        with open(filename, 'w') as f:
            f.write(content)
        print(f'Fixed: {filename}')
    else:
        print(f'No match: {filename}')
        print(f'  Content starts with: {repr(content[:50])}')
        print(f'  Looking for: {repr(corrupted[:50])}')
