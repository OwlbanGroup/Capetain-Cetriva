"""
Banking utilities module for handling account generation, routing, validation,
ACH payments, and Plaid integrations.
"""

import os
import logging
from unittest.mock import MagicMock
from typing import Optional, Dict, Any, Union

from generate_account_number import (
    generate_account_number,
    is_valid_account_number,
)
from get_routing_number import get_routing_number
from validate_routing_number import validate_routing_number
from plaid_integration import PlaidIntegration
from ach_payments import ACHPayments
from ai_models.market_trend_analysis import MarketTrendAnalysis
from nvidia_integration import nvidia_integration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BankingUtils:
    """
    A utility class for banking operations including account generation,
    routing number retrieval, validation, ACH payments, and Plaid integrations.
    """
    # Patch PlaidIntegration to avoid real API calls during tests
    plaid_integration: Union[MagicMock, PlaidIntegration] = (
        MagicMock() if os.getenv('TESTING') == '1' else PlaidIntegration()
    )

    ach_payments = ACHPayments()

    @staticmethod
    def generate_account(length: int = 9) -> Optional[str]:
        """
        Generate a valid bank account number.

        Args:
            length (int): Length of the account number.

        Returns:
            Optional[str]: Generated account number or None if validation fails.
        """
        try:
            account_number = generate_account_number(length)
            if not is_valid_account_number(account_number):
                logger.error(
                    "Generated account number failed validation: %s",
                    account_number
                )
                return None
            logger.info("Generated account number: %s", account_number)
            return account_number
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Error generating account number: %s", e)
            return None

    @staticmethod
    def get_routing(bank_name: str) -> Optional[str]:
        """
        Retrieve the routing number for a given bank name.
        
        Args:
            bank_name (str): Name of the bank.

        Returns:
            Optional[str]: Routing number or None if retrieval fails.
        """
        try:
            routing_number = get_routing_number(bank_name)
            logger.info("Retrieved routing number for %s: %s", bank_name, routing_number)
            return routing_number
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Error retrieving routing number for %s: %s", bank_name, e)
            return None

    @staticmethod
    def validate_routing(routing_number: str) -> bool:
        """
        Validate a routing number.

        Args:
            routing_number (str): Routing number to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            is_valid = validate_routing_number(routing_number)
            logger.info(
                "Routing number %s validation result: %s",
                routing_number, is_valid
            )
            return is_valid
        except Exception as e:
            logger.error("Error validating routing number %s: %s", routing_number, e)
            return False

    @classmethod
    def create_ach_payment(cls, account_number: str, routing_number: str, amount: float, description: str = "") -> Optional[Dict[str, Any]]:
        """
        Create an ACH payment.

        Args:
            account_number (str): Account number.
            routing_number (str): Routing number.
            amount (float): Payment amount.
            description (str): Payment description.

        Returns:
            Optional[Dict[str, Any]]: Payment response or None if creation fails.
        """
        try:
            response = cls.ach_payments.create_payment(
                account_number,
                routing_number,
                amount,
                description,
            )
            logger.info("ACH payment created: %s", response)
            return response
        except Exception as e:
            logger.error("Error creating ACH payment: %s", e)
            return None

    @classmethod
    def get_ach_payment_status(cls, transaction_id: str) -> Optional[Union[str, Dict[str, Any]]]:
        """
        Get the status of an ACH payment.

        Args:
            transaction_id (str): Transaction ID.

        Returns:
            Optional[Union[str, Dict[str, Any]]]: Payment status or None if retrieval fails.
        """
        try:
            status = cls.ach_payments.get_payment_status(transaction_id)
            logger.info("ACH payment status: %s", status)
            return status
        except Exception as e:
            logger.error("Error getting ACH payment status: %s", e)
            return None

    @classmethod
    def create_plaid_link_token(cls, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Create a Plaid link token.

        Args:
            user_id (str): User identifier.

        Returns:
            Optional[Dict[str, Any]]: Link token response or None if creation fails.
        """
        try:
            response = cls.plaid_integration.create_link_token(user_id)
            logger.info("Plaid link token created: %s", response)
            return response
        except Exception as e:
            logger.error("Error creating Plaid link token: %s", e)
            return None

    @classmethod
    def exchange_plaid_public_token(cls, public_token: str) -> Optional[Dict[str, Any]]:
        """
        Exchange a Plaid public token for an access token.

        Args:
            public_token (str): Public token.

        Returns:
            Optional[Dict[str, Any]]: Access token response or None if exchange fails.
        """
        try:
            response = cls.plaid_integration.exchange_public_token(public_token)
            logger.info("Plaid public token exchanged: %s", response)
            return response
        except Exception as e:
            logger.error("Error exchanging Plaid public token: %s", e)
            return None

    @classmethod
    def get_plaid_accounts(cls, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve Plaid accounts linked to the access token.

        Args:
            access_token (str): Access token.

        Returns:
            Optional[Dict[str, Any]]: Accounts information or None if retrieval fails.
        """
        try:
            response = cls.plaid_integration.get_accounts(access_token)
            logger.info("Plaid accounts retrieved: %s", response)
            return response
        except Exception as e:
            logger.error("Error retrieving Plaid accounts: %s", e)
            return None

    @classmethod
    def spend_profits_for_oscar(cls, amount: float, description: str = "", account_number: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Create an ACH payment to allow Oscar Broome to spend profits from the project.

        Args:
            amount (float): Amount to spend.
            description (str): Optional payment description.
            account_number (Optional[str]): Oscar's bank account number. If None, generate a valid account number.

        Returns:
            Optional[Dict[str, Any]]: Payment response or None if creation fails.
        """
        routing_number = "021000021"  # Capetain Private AI Bank routing number
        if account_number is None:
            account_number = cls.generate_account()
            if account_number is None:
                logger.error("Failed to generate a valid account number for Oscar Broome.")
                return None
        return cls.create_ach_payment(account_number, routing_number, amount, description)

    @classmethod
    def allocate_and_spend_profits(cls, total_amount: float, description: str = "") -> Dict[str, Optional[Dict[str, Any]]]:
        """
        Allocate the total profits according to the investment thesis and corporate breakdown,
        then spend the allocated amounts via ACH payments.

        Allocation percentages based on corporate_breakdown.md and investment_thesis.md:
        - 60% Alternative Assets (Private Equity, Real Estate, Commodities)
        - 30% Public Equities (AI-enhanced stock selection)
        - 10% Digital Assets (Blockchain-based investments)

        Args:
            total_amount (float): Total profit amount to allocate and spend.
            description (str): Optional description for payments.

        Returns:
            Dict[str, Optional[Dict[str, Any]]]: Mapping of asset class to payment response or None if failed.
        """
        allocations = {
            "Alternative Assets": 0.60,
            "Public Equities": 0.30,
            "Digital Assets": 0.10,
        }

        responses: Dict[str, Optional[Dict[str, Any]]] = {}
        for asset_class, percentage in allocations.items():
            amount = total_amount * percentage
            if asset_class == "Public Equities":
                # AI-enhanced stock selection using GPU-accelerated model
                nvidia_integration.log_project_status("Equity Allocation")
                mta = MarketTrendAnalysis(ticker="NVDA")  # NVIDIA stock for AI theme
                mta.download_data()
                mta.feature_engineering()
                mta.train_model()
                # Predict trend on latest data (simplified: if last target is 1, positive)
                if mta.data is not None and not mta.data.empty and mta.data["Target"].iloc[-1] == 1:
                    logger.info("AI prediction: Positive trend for NVDA, allocating full equities.")
                else:
                    amount *= 0.5  # Reduce allocation if negative trend
                    logger.info("AI prediction: Negative trend for NVDA, reducing equities allocation.")

            payment_description = "%s - Allocation to %s" % (description, asset_class)
            # For demonstration, generate a new account number for each allocation
            account_number = cls.generate_account()
            if account_number is None:
                logger.error("Failed to generate account number for %s allocation.", asset_class)
                responses[asset_class] = None
                continue
            response = cls.create_ach_payment(account_number, "021000021", amount, payment_description)
            responses[asset_class] = response
            logger.info("Allocated %s to %s with response: %s", amount, asset_class, response)

        return responses


if __name__ == "__main__":
    # Example usage
    bank_utils = BankingUtils()
    account = bank_utils.generate_account(10)
    print(f"Generated Account Number: {account}")

    bank_name = "Capetain Cetriva"
    routing = bank_utils.get_routing(bank_name)
    print(f"Routing Number for {bank_name}: {routing}")

    is_valid = bank_utils.validate_routing(routing if routing else "")
    print(f"Is Routing Number Valid? {is_valid}")

    # ACH payment example
    if account and routing:
        ach_response = bank_utils.create_ach_payment(account, routing, 100.0, "Test ACH payment")
        print(f"ACH Payment Response: {ach_response}")
    else:
        print("Cannot create ACH payment: missing account or routing number")

    # Plaid example (requires valid tokens)
    user_id = "user123"
    link_token_response = bank_utils.create_plaid_link_token(user_id)
    print(f"Plaid Link Token Response: {link_token_response}")

    # Oscar Broome spend profits example
    oscar_payment_response = bank_utils.spend_profits_for_oscar(5000.0, "Spending profits for Oscar Broome")
    print(f"Oscar Broome Spend Profits Payment Response: {oscar_payment_response}")

    # Allocate and spend profits example
    allocation_responses = bank_utils.allocate_and_spend_profits(10000.0, "Profit allocation for Oscar Broome")
    print(f"Profit Allocation Responses: {allocation_responses}")
