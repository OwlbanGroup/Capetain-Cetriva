# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Testing Infrastructure (Round 1)
- `conftest.py` with central TESTING mode setup and shared mock fixtures:
  `mock_torch`, `mock_plaid_api`, `mock_nvidia`, `mock_market_trend`
- `test_testing_guard.py` — 11 tests verifying TESTING mode guard behavior
- `test_import_performance.py` — 3 benchmark tests for import performance
- `run_tests_fast.py` — convenience script for fast test execution in TESTING mode

#### Documentation & Configuration (Round 2)
- `README.md` updates:
  - CI status badge
  - TESTING mode documentation table
  - Fixture documentation
  - Pytest marker documentation
  - Fast test runner instructions
- `CONTRIBUTING.md` — complete contributor guide with TESTING mode, fixtures, and quality gates
- `TOPOLOGY.md` — Oscar compensation flow with period parameter
- `pytest.ini` — timeout, coverage (term/XML/HTML), pytest markers
- `.coveragerc` — branch coverage, mock line exclusions
- `requirements-dev.txt` — added `pytest-timeout`, `pytest-cov`, `isort`
- `.github/workflows/ci.yml` — pytest-timeout, coverage artifact upload

#### Type Stubs & Tooling (Round 3)
- Type stub files (`.pyi`):
  - `plaid_integration.pyi`
  - `banking_utils.pyi`
  - `e2e_nvidia_blackwell_integration.pyi`
- `mypy.ini` — type checking configuration
- `.flake8` — flake8 configuration (max-line-length=120)
- `py.typed` — PEP 561 marker for type hinting support
- `tox.ini` — multi-environment testing (lint, mypy, coverage, py310/311/312, fast)
- `scripts/` directory with helper scripts:
  - `test_fast.sh` — fast TESTING mode test runner
  - `check_types.sh` — mypy type checking
  - `validate_ci.sh` — full CI validation
  - `setup_hooks.sh` — git pre-commit hook installation
- `hooks/pre-commit` — git pre-commit hook
- `.github/coverage.yml` — coverage reporting workflow

### Changed
- `plaid_integration.py` — added TESTING guard for Plaid SDK imports
- `test_plaid_integration.py` — refactored tests for TESTING mode compatibility
- `.github/workflows/ci.yml` — added pytest plugin verification, `--tb=short`, coverage config
- `.pylintrc` — added scripts/hook exclusions, test path ignores
- `.gitignore` — added `htmlcov/` exclusion
- `pytest.ini` — added `requires_torch`/`requires_plaid` markers, `--tb=short`, HTML coverage
- `.coveragerc` — added `.pyi` files to omit list

### Removed
- Temporary fix scripts (fix_conftest.py, fix_test_guard.py, fix_ci.py)
- Temporary output files (test_output.txt, etc.)

## [0.1.0] - Initial Release

- AI-driven banking operations system
- NVIDIA Blackwell GPU integration
- Plaid banking API integration
- Oscar Broome compensation calculation
- OpenShift deployment manifests
