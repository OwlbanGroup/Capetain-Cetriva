import re

files_to_fix = [
    'test_banking_utils.py',
    'test_banking_utils_refactored.py',
    'test_banking_utils_edge_cases.py',
    'test_banking_utils_allocate_profits.py',
    'test_banking_utils_extended.py',
    'test_performance_and_edge_cases.py',
]

for filename in files_to_fix:
    with open(filename, 'r') as f:
        content = f.read()
    
    # Fix broken docstring at the beginning
    # Pattern: """\r\n\r\nimport os...\r\n\r\n"Tests for some description."""
    # Should be: """Tests for some description."""\r\n\r\nimport os...
    
    # Match the broken pattern
    broken_pattern = re.compile(
        r'^"""\r?\n\r?\nimport os\r?\n'
        r'os\.environ\.setdefault\("TESTING", "1"\)\r?\n'
        r'os\.environ\.setdefault\("PYTHONWARNINGS", "ignore"\)\r?\n'
        r'\r?\n'
        r'"Tests for (.+?)"""',
        re.MULTILINE
    )
    
    def fix_match(m):
        doc = m.group(1).strip()
        return f'"""Tests for {doc}."""\r\n\r\nimport os\r\nos.environ.setdefault("TESTING", "1")\r\nos.environ.setdefault("PYTHONWARNINGS", "ignore")\r\n'
    
    new_content = broken_pattern.sub(fix_match, content)
    
    # Also handle the pattern in test_performance_and_edge_cases.py where docstring is followed by imports
    # Pattern: """some text."""\r\n\r\nimport os\r\n...
    # But the docstring might have been correct already
    
    if new_content != content:
        with open(filename, 'w') as f:
            f.write(new_content)
        print(f'Fixed docstring in: {filename}')
    else:
        print(f'No broken docstring pattern in: {filename}')
        
        # Check what the file looks like
        first_10 = content[:200]
        print(f'  First 200 chars: {repr(first_10)}')
