import os, sys, subprocess

env = dict(os.environ)
env['TESTING'] = '1'
env['ACH_API_KEY'] = 'test-ci-key'
env['PYTHONWARNINGS'] = 'ignore'

# Run pytest with debug
result = subprocess.run(
    [sys.executable, '-m', 'pytest', '--no-cov', '-x', '--tb=short', '-v',
     '-p', 'no:cacheprovider',
     'test_banking_utils.py::TestBankingUtils::test_generate_account_valid'],
    env=env, capture_output=True, text=True,
    cwd=os.getcwd()
)
print(result.stdout[-2000:])
print('STDERR:', result.stderr[:500])
