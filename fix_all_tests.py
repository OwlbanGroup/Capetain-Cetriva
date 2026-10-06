import os

# Files that were corrupted by the fix_test_guards.py script
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
    
    original = content
    
    # Fix the broken docstring pattern
    if content.startswith('"""\r\n') or content.startswith('"""\n'):
        # The pattern is:
        # """\r\n\r\nimport os\r\nos.environ.setdefault("TESTING", "1")\r\n...\r\n\r\n"Tests for test banking utils.""""
        # We need to convert it to:
        # """Tests for test banking utils."""\r\n\r\nimport os\r\nos.environ.setdefault("TESTING", "1")\r\n...
        
        # Find the broken docstring
        lines = content.split('\n')
        new_lines = []
        i = 0
        fixed = False
        while i < len(lines):
            line = lines[i]
            if line.strip() == '"""' and i > 0 and i < 5:
                # This is a broken opening triple quote
                # Look for the docstring content
                doc = ""
                j = i + 1
                while j < len(lines):
                    if '"Tests for test banking utils.' in lines[j]:
                        doc = lines[j].strip()
                        # Extract just the docstring text
                        import re
                        match = re.search(r'"([^"]*)"', doc)
                        if match:
                            doc_content = match.group(1)
                        else:
                            doc_content = doc.replace('"""', '').strip()
                        new_lines.append(f'"""{doc_content}"""')
                        i = j + 1
                        fixed = True
                        break
                    j += 1
                if not fixed:
                    new_lines.append(line)
                    i += 1
                else:
                    i = j + 1
                continue
            new_lines.append(line)
            i += 1
        
        content = '\n'.join(new_lines)
    
    # Normalize line endings to \n
    content = content.replace('\r\n', '\n')
    
    if content != original:
        with open(filename, 'w') as f:
            f.write(content)
        print(f'Fixed: {filename}')
    else:
        print(f'No changes needed: {filename}')
