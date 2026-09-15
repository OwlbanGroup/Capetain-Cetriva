import pathlib
content = open('template.txt').read()
pathlib.Path('CreateRevenueDisbursementFile.py').write_text(content)
print('Done')
