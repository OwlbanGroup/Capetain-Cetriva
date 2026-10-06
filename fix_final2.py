import re

files_to_fix = [
    'test_banking_utils.py',
    'test_banking_utils_refactored.py',
    'test_banking_utils_edge_cases.py',
    'test_banking_utils_allocate_profits.py',
    'test_banking_utils_extended.py',
]

for filename in files_to_fix:
    with open(filename, 'rb') as f:
        raw = f.read()
    content = raw.decode('utf-8').replace('\r\n', '\n')
    
    # Fix the broken docstring pattern
    # Old: """\n\nimport os\n...\"Tests for description.\"\"\"
    # The docstring text starts with a single quote and ends with triple quotes
    
    pattern = re.compile(
        r'^"""\n\nimport os\n'
        r'os\.environ\.setdefault\("TESTING", "1"\)\n'
        r'os\.environ\.setdefault\("PYTHONWARNINGS", "ignore"\)\n'
        r'\n'
        r'"([^"]+)"\"\"\"',
        re.MULTILINE
    )
    
    def replace(m):
        doc_text = m.group(1)
        return f'"""{doc_text}."""\n\nimport os\nos.environ.setdefault("TESTING", "1")\nos.environ.setdefault("PYTHONWARNINGS", "ignore")\n'
    
    new_content = pattern.sub(replace, content)
    
    if new_content != content:
        with open(filename, 'w') as f:
            f.write(new_content)
        print(f'Fixed: {filename}')
    else:
        print(f'No match: {filename}')
