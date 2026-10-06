"""Type stub for plaid_integration module.

Provides type information for the PlaidIntegration class regardless
of whether TESTING mode is enabled. This file helps IDEs and type
checkers understand the module interface.
"""

import logging
from typing import Any, Dict, Optional

# These names are either real (non-TESTING mode) or MagicMock (TESTING mode)
# The stub provides consistent typing in both cases.
plaid_api: Any
Products: Any
CountryCode: Any
LinkTokenCreateRequest: Any
LinkTokenCreateRequestUser: Any
TransactionsGetRequest: Any
TransactionsGetRequestOptions: Any
ItemGetRequest: Any
ItemRemoveRequest: Any
ItemAccessTokenInvalidateRequest: Any
Configuration: Any

logger: logging.Logger


class PlaidIntegration:
    """Wrapper around the Plaid API for account linking and data retrieval."""

    def __init__(self) -> None: ...
    def create_link_token(self, user_id: str) -> Optional[Dict[str, Any]]: ...
    def exchange_public_token(self, public_token: str) -> Optional[Dict[str, Any]]: ...
    def get_accounts(self, access_token: str) -> Optional[Dict[str, Any]]: ...
    def get_transactions(
        self,
        access_token: str,
        start_date: str,
        end_date: str,
        options: Any = ...,
    ) -> Optional[Dict[str, Any]]: ...
    def get_item(self, access_token: str) -> Optional[Dict[str, Any]]: ...
    def remove_item(self, access_token: str) -> Optional[Dict[str, Any]]: ...
    def invalidate_access_token(self, access_token: str) -> Optional[Dict[str, Any]]: ...
