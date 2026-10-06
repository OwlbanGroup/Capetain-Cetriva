# Capetain Cetriva AI Hybrid Fund

![CI](https://github.com/OwlbanGroup/Capetain-Cetriva/actions/workflows/ci.yml/badge.svg?branch=main)

AI-driven banking operations and market analysis system integrating NVIDIA
Blackwell GPU acceleration, banking utilities, and OpenShift-based deployment.

## Setup

```bash
pip install -r requirements.txt       # runtime dependencies
pip install -r requirements-dev.txt   # lint / type-check tooling
```

## Quality gates

Linting is enforced on every commit via a pre-commit hook (flake8,
config in `.flake8`). Enable it after cloning:

```bash
scripts/setup_hooks.sh        # sets git config core.hooksPath=hooks
```

Bypass in an emergency with `git commit --no-verify`.

### Manual checks

```bash
python -m flake8                          # lint (0 issues expected)
python -m pytest test_banking_utils.py test_oscar_compensation.py    # run tests
```

## Key entry points

| File | Purpose |
| --- | --- |
| `account_routing_demo.py` | Account/routing number demo |
| `banking_utils.py` | Unified `BankingUtils` interface |
| `oscar_compensation.py` | Oscar Broome compensation calculation and ACH disbursement |
| `e2e_nvidia_blackwell_integration.py` | Full E2E pipeline orchestration |
| `docs/manifests/` | OpenShift/KubeVirt deployment manifests |
| `TOPOLOGY.md` | System architecture and topology |

## TESTING mode

Set `TESTING=1` to run tests without installing heavy ML dependencies
(PyTorch, scikit-learn, pynvml). Modules that import torch are replaced
with `MagicMock` automatically when this variable is set:

| Module | Guarded imports |
| --- | --- |
| `banking_utils.py` | `ai_models.market_trend_analysis`, `nvidia_integration` |
| `e2e_nvidia_blackwell_integration.py` | `ai_models.market_trend_analysis`, `nvidia_integration` |
| `plaid_integration.py` | `plaid.api`, `plaid.model`, `plaid.configuration` |
| `ai_models/test_market_trend_analysis.py` | `ai_models.market_trend_analysis` |

### Running tests in TESTING mode

```bash
TESTING=1 python -m pytest -q
# or
TESTING=1 python -m unittest discover -s . -p "test_*.py"
```

In CI, the `test` job runs both with torch (`testing_mode: full`)
and without (`testing_mode: mocked`, which sets `TESTING=1`),
providing fast feedback on every pull request.

### Available test fixtures

The `conftest.py` module provides the following shared fixtures for
use in tests:

| Fixture | Description |
| --- | --- |
| `mock_torch` | A fresh `MagicMock` replacing `torch` in TESTING mode |
| `mock_plaid_api` | A fresh `MagicMock` replacing the Plaid SDK |
| `mock_nvidia` | A fresh `MagicMock` replacing `nvidia_integration` |
| `mock_market_trend` | A fresh `MagicMock` replacing `MarketTrendAnalysis` |

Example usage in a test:

```python
def test_my_function(mock_torch, mock_plaid_api):
    import my_module
    # my_module uses MagicMock instead of real torch/plaid
    result = my_module.run()
    mock_plaid_api.assert_called()
```

Custom pytest markers:

| Marker | Description |
| --- | --- |
| `slow` | Marks tests as slow (not skipped by default) |
| `integration` | Marks integration tests requiring external services |
| `requires_torch` | Skipped in TESTING mode (requires real torch) |
| `requires_plaid` | Skipped in TESTING mode (requires real Plaid SDK) |

### Fast test runner

For quick local development, use the fast test runner script:

```bash
python run_tests_fast.py                        # all tests
python run_tests_fast.py -v                     # verbose output
python run_tests_fast.py test_plaid_integration  # specific test
```


## Oscar Broome Compensation

### Fee Structure
- **Management Fee**: 2% of Assets Under Management (AUM)
- **Performance Fee**: 20% of returns above 8% annual hurdle rate
- **Ownership**: 100% of fees allocated to Oscar

### Usage

```python
from revenue_disbursement import RevenueDisbursement

# Default annual compensation
result = RevenueDisbursement.allocate_oscar_compensation(
    aum=150_000_000,
    returns=22_500_000,
)

# Quarterly compensation
result = RevenueDisbursement.allocate_oscar_compensation(
    aum=150_000_000,
    returns=5_000_000,
    period="Q1 2024",
    description="Q1 2024 Oscar Broome Compensation",
)

# Semi-annual compensation
result = RevenueDisbursement.allocate_oscar_compensation(
    aum=150_000_000,
    returns=12_000_000,
    period="H1 2024",
    description="Semi-annual Oscar Broome Compensation",
)
```

The `period` parameter is included in the ACH payment description:
`Oscar Broome Compensation (Q1 2024)`
