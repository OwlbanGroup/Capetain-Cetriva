# Contributing to Capetain Cetriva AI Hybrid Fund

Thank you for your interest in contributing! This document covers the essentials.

## Quick Start

```bash
# Clone and install
git clone https://github.com/OwlbanGroup/Capetain-Cetriva.git
cd Capetain-Cetriva
pip install -r requirements.txt -r requirements-dev.txt

# Run tests in fast TESTING mode (no torch/plaid required)
TESTING=1 python -m pytest -q

# Or use the fast runner
python run_tests_fast.py
```

## TESTING Mode

Set `TESTING=1` to run tests without installing heavy ML dependencies:

| Module | Guarded imports |
| --- | --- |
| `banking_utils.py` | `ai_models.market_trend_analysis`, `nvidia_integration` |
| `e2e_nvidia_blackwell_integration.py` | `ai_models.market_trend_analysis`, `nvidia_integration` |
| `plaid_integration.py` | `plaid.api`, `plaid.model`, `plaid.configuration` |

In TESTING mode, these modules are replaced with `MagicMock` automatically.

## Type Markers

Use these pytest markers in your tests:

| Marker | Description |
| --- | --- |
| `@pytest.mark.slow` | Mark tests as slow |
| `@pytest.mark.integration` | Integration tests requiring external services |
| `@pytest.mark.requires_torch` | Skipped in TESTING mode (requires real torch) |
| `@pytest.mark.requires_plaid` | Skipped in TESTING mode (requires real Plaid SDK) |

Example:

```python
import pytest

@pytest.mark.requires_torch
def test_gpu_acceleration():
    import torch
    # This test is skipped when TESTING=1
    assert torch.cuda.is_available()
```

## Available Fixtures

The `conftest.py` module provides these shared fixtures:

| Fixture | Description |
| --- | --- |
| `mock_torch` | A fresh `MagicMock` replacing `torch` in TESTING mode |
| `mock_plaid_api` | A fresh `MagicMock` replacing the Plaid SDK |
| `mock_nvidia` | A fresh `MagicMock` replacing `nvidia_integration` |
| `mock_market_trend` | A fresh `MagicMock` replacing `MarketTrendAnalysis` |

## Quality Gates

### Linting

```bash
python -m isort --check-only .    # import ordering
python -m flake8                    # style and errors (max-line=120)
python -m pylint --rcfile=.pylintrc *.py
python -m mypy *.py --follow-imports=skip
```

### Pre-commit Hooks

```bash
scripts/setup_hooks.sh    # installs git hooks
git commit --no-verify    # bypass in emergencies only
```

### Testing

```bash
# Full test suite (requires torch)
python -m pytest

# Fast test suite (TESTING=1, no torch)
TESTING=1 python -m pytest -q

# Run specific test file
python -m pytest test_plaid_integration.py -v

# Run with coverage
python -m pytest --cov=. --cov-report=term-missing --cov-report=html
```

## Multi-Environment Testing

```bash
# Using tox
tox                        # run all environments
tox -e py310              # Python 3.10 only
tox -e lint               # lint checks
tox -e mypy               # type checking
tox -e coverage           # coverage report
```

## Code Style

- Follow PEP 8 (flake8 enforced, max line 120 chars)
- Use type hints (`-> None`, `Optional[Dict[str, Any]]`, etc.)
- Add docstrings to all public functions and classes
- Use `unittest.mock.MagicMock` for mocked dependencies in tests

## Pull Request Process

1. Ensure all quality gates pass
2. Add tests for new functionality
3. Update documentation as needed
4. CI will verify linting, type checking, and tests

## Need Help?

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
