# Capetain Cetriva AI Hybrid Fund

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
python -m pylint <file>                   # deep static analysis
python -m mypy <file> --ignore-missing-imports --follow-imports=skip
python -m pytest test_banking_utils.py    # run tests
```

## Key entry points

| File | Purpose |
| --- | --- |
| `account_routing_demo.py` | Account/routing number demo |
| `banking_utils.py` | Unified `BankingUtils` interface |
| `e2e_nvidia_blackwell_integration.py` | Full E2E pipeline orchestration |
| `docs/manifests/` | OpenShift/KubeVirt deployment manifests |
| `TOPOLOGY.md` | System architecture and topology |
