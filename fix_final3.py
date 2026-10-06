files_to_fix = [
    'test_banking_utils.py',
    'test_banking_utils_refactored.py',
    'test_banking_utils_edge_cases.py',
    'test_banking_utils_allocate_profits.py',
    'test_banking_utils_extended.py',
]

old_patterns = [
    # test_banking_utils.py
    ('"""\n\nimport os\nos.environ.setdefault("TESTING", "1")\nos.environ.setdefault("PYTHONWARNINGS", "ignore")\n\n"Tests for test banking utils."""', 
     '"""Tests for test banking utils."""\n\nimport os\nos.environ.setdefault("TESTING", "1")\nos.environ.setdefault("PYTHONWARNINGS", "ignore")\n'),
    # test_banking_utils_refactored.py
    ('"""\n\nimport os\nos.environ.setdefault("TESTING", "1")\nos.environ.setdefault("PYTHONWARNINGS", "ignore")\n\n"Unit tests for BankingUtils.generate_account using mocked dependencies."""',
     '"""Unit tests for BankingUtils.generate_account using mocked dependencies."""\n\nimport os\nos.environ.setdefault("TESTING", "1")\nos.environ.setdefault("PYTHONWARNINGS", "ignore")\n'),
    # test_banking_utils_edge_cases.py
    ('"""\n\nimport os\nos.environ.setdefault("TESTING", "1")\nos.environ.setdefault("PYTHONWARNINGS", "ignore")\n\n"Tests for test banking utils edge cases."""',
     '"""Tests for test banking utils edge cases."""\n\nimport os\nos.environ.setdefault("TESTING", "1")\nos.environ.setdefault("PYTHONWARNINGS", "ignore")\n'),
    # test_banking_utils_allocate_profits.py
    ('"""\n\nimport os\nos.environ.setdefault("TESTING", "1")\nos.environ.setdefault("PYTHONWARNINGS", "ignore")\n\n"Tests for test banking utils allocate profits."""',
     '"""Tests for test banking utils allocate profits."""\n\nimport os\nos.environ.setdefault("TESTING", "1")\nos.environ.setdefault("PYTHONWARNINGS", "ignore")\n'),
    # test_banking_utils_extended.py
    ('"""\n\nimport os\nos.environ.setdefault("TESTING", "1")\nos.environ.setdefault("PYTHONWARNINGS", "ignore")\n\n"Tests for test banking utils extended."""',
     '"""Tests for test banking utils extended."""\n\nimport os\nos.environ.setdefault("TESTING", "1")\nos.environ.setdefault("PYTHONWARNINGS", "ignore")\n'),
]

for filename in files_to_fix:
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8').replace('\r\n', '\n')
    
    fixed = False
    for old, new in old_patterns:
        if old in content:
            content = content.replace(old, new, 1)
            fixed = True
            break
    
    if fixed:
        with open(filename, 'w', newline='\n') as f:
            f.write(content)
        print(f'Fixed: {filename}')
    else:
        print(f'No match: {filename}')
