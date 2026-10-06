"""pytest configuration for TESTING mode and shared fixtures."""

import os
from unittest.mock import MagicMock

import pytest

# Enable TESTING mode before any application module imports
os.environ.setdefault("TESTING", "1")


def pytest_configure(config):
    """Set up TESTING environment for all tests."""
    os.environ["TESTING"] = "1"
    os.environ.setdefault("ACH_API_KEY", "test-ci-key")
    os.environ.setdefault("PYTHONWARNINGS", "ignore")


def pytest_collection_modifyitems(config, items):
    """Auto-skip tests requiring external services in TESTING mode.

    In TESTING mode (CI), we mock torch and plaid, so tests marked with
    requires_torch or requires_plaid use MagicMocks and should be skipped
    unless the user explicitly sets FORCE_REAL_DEPS=1.
    """
    if os.getenv("FORCE_REAL_DEPS") != "1":
        skip_marker = pytest.mark.skip(
            reason="Skipped: requires real torch/plaid (set FORCE_REAL_DEPS=1 to run)"
        )
        for item in items:
            if (
                "requires_torch" in item.keywords
                or "requires_plaid" in item.keywords
            ):
                item.add_marker(skip_marker)


@pytest.fixture
def mock_torch():
    """Provide a fresh MagicMock for torch."""
    return MagicMock()


@pytest.fixture
def mock_plaid_api():
    """Provide a fresh MagicMock for plaid_api."""
    return MagicMock()


@pytest.fixture
def mock_nvidia():
    """Provide a fresh MagicMock for nvidia_integration."""
    return MagicMock()


@pytest.fixture
def mock_market_trend():
    """Provide a fresh MagicMock for MarketTrendAnalysis."""
    return MagicMock()
