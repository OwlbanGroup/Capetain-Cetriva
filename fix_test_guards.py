import os

files_to_fix = [
    'test_banking_utils.py',
    'test_banking_utils_refactored.py',
    'test_banking_utils_edge_cases.py',
    'test_banking_utils_allocate_profits.py',
    'test_banking_utils_extended.py',
]

guard = '''import os
os.environ.setdefault("TESTING", "1")
os.environ.setdefault("PYTHONWARNINGS", "ignore")

'''

for filename in files_to_fix:
    with open(filename, 'r') as f:
        content = f.read()
    
    if 'TESTING' not in content:
        content = guard + content
        
        with open(filename, 'w') as f:
            f.write(content)
        print(f'Fixed: {filename}')
    else:
        print(f'Already has TESTING guard: {filename}')
