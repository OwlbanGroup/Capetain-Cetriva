"""Type stub for banking_utils module.

Provides type information for the BankingUtils class regardless
of whether TESTING mode is enabled.
"""

import logging
from typing import Any, Dict, Optional, Union
from unittest.mock import MagicMock

from ach_payments import ACHPayments
from generate_account_number import (generate_account_number,
                                     is_valid_account_number)
from get_routing_number import get_routing_number
from validate_routing_number import validate_routing_number

# Real or MagicMock depending on TESTING mode
PlaidIntegration: Any
MarketTrendAnalysis: Any
nvidia_integration: Any

logger: logging.Logger


class BankingUtils:
    """A utility class for banking operations."""

    plaid_integration: Union[MagicMock, Any]
    ach_payments: ACHPayments

    @staticmethod
    def generate_account(length: int = 9) -> Optional[str]: ...
    @staticmethod
    def get_routing(bank_name: str) -> Optional[str]: ...
    @staticmethod
    def create_ach_payment(
        account_number: str,
        routing_number: str,
        amount: float,
        description: str,
    ) -> Optional[Dict[str, Any]]: ...
    @staticmethod
    def validate_routing(routing_number: str) -> bool: ...
    @staticmethod
    def create_plaid_link_token(user_id: str) -> Optional[Dict[str, Any]]: ...
    @staticmethod
    def get_plaid_accounts(access_token: str) -> Optional[Dict[str, Any]]: ...
    @staticmethod
    def get_plaid_transactions(
        access_token: str,
        start_date: str,
        end_date: str,
        options: Any = ...,
    ) -> Optional[Dict[str, Any]]: ...
    @staticmethod
    def spend_profits_for_oscar(amount: float, description: str) -> Optional[Dict[str, Any]]: ...
    @staticmethod
    def allocate_and_spend_profits(
        total_amount: float,
        description: str,
    ) -> Dict[str, Optional[Dict[str, Any]]]: ...
