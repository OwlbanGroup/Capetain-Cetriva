import re

files = [
    'test_banking_utils.py',
    'test_banking_utils_refactored.py',
    'test_banking_utils_edge_cases.py',
    'test_banking_utils_allocate_profits.py',
    'test_banking_utils_extended.py',
]

guard_start = 'import os\nos.environ.setdefault("TESTING", "1")\nos.environ.setdefault("PYTHONWARNINGS", "ignore")\n\n'

for filename in files:
    with open(filename, 'r') as f:
        content = f.read()
    
    # Check if guard is before docstring
    if content.startswith(guard_start) and '"""' in content[:200]:
        # Extract the docstring and move it before the guard
        rest = content[len(guard_start):]
        # Find the docstring
        match = re.match(r'("[^"]*"|\'[^\']*\')', rest, re.DOTALL)
        if match:
            docstring = match.group(1)
            after_docstring = rest[len(docstring):]
            new_content = docstring + '\n\n' + guard_start + after_docstring.lstrip('\n')
            with open(filename, 'w') as f:
                f.write(new_content)
            print(f'Fixed order in {filename}')
        else:
            print(f'No docstring found in {filename}')
    else:
        print(f'Already correct order or no guard in {filename}')
