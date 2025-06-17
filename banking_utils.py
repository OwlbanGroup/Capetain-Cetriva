import os
import logging
from unittest.mock import MagicMock

from generate_account_number import (
    generate_account_number,
    is_valid_account_number,
)
from get_routing_number import get_routing_number
from validate_routing_number import validate_routing_number
from plaid_integration import PlaidIntegration


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BankingUtils:
    # Patch PlaidIntegration to avoid real API calls during tests
    if os.getenv('TESTING') == '1':
        plaid_integration = MagicMock()
    else:
        plaid_integration = PlaidIntegration()

    @staticmethod
    def generate_account(length=9):
        """
        Generate a valid bank account number.

        Args:
            length (int): Length of the account number.

        Returns:
            str or None: Generated account number or None if validation fails.
        """
        try:
            account_number = generate_account_number(length)
            if not is_valid_account_number(account_number):
                logger.error(
                    f"Generated account number failed validation: {account_number}"
                )
                return None
            logger.info(f"Generated account number: {account_number}")
            return account_number
        except Exception as e:
            logger.error(f"Error generating account number: {e}")
            return None

    @staticmethod
    def get_routing(bank_name):
        """
        Retrieve the routing number for a given bank name.

        Args:
            bank_name (str): Name of the bank.

        Returns:
            str or None: Routing number or None if retrieval fails.
        """
        try:
            routing_number = get_routing_number(bank_name)
            logger.info(f"Retrieved routing number for {bank_name}: {routing_number}")
            return routing_number
        except Exception as e:
            logger.error(f"Error retrieving routing number for {bank_name}: {e}")
            return None

    @staticmethod
    def validate_routing(routing_number):
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
                f"Routing number {routing_number} validation result: {is_valid}"
            )
            return is_valid
        except Exception as e:
            logger.error(f"Error validating routing number {routing_number}: {e}")
            return False

    @classmethod
    def create_ach_payment(cls, account_number, routing_number, amount, description=""):
        """
        Create an ACH payment.

        Args:
            account_number (str): Account number.
            routing_number (str): Routing number.
            amount (float): Payment amount.
            description (str): Payment description.

        Returns:
            dict or None: Payment response or None if creation fails.
        """
        try:
            response = cls.ach_payments.create_payment(
                account_number,
                routing_number,
                amount,
                description,
            )
            logger.info(f"ACH payment created: {response}")
            return response
        except Exception as e:
            logger.error(f"Error creating ACH payment: {e}")
            return None

    @classmethod
    def get_ach_payment_status(cls, transaction_id):
        """
        Get the status of an ACH payment.

        Args:
            transaction_id (str): Transaction ID.

        Returns:
            str or None: Payment status or None if retrieval fails.
        """
        try:
            status = cls.ach_payments.get_payment_status(transaction_id)
            logger.info(f"ACH payment status: {status}")
            return status
        except Exception as e:
            logger.error(f"Error getting ACH payment status: {e}")
            return None

    @classmethod
    def create_plaid_link_token(cls, user_id):
        """
        Create a Plaid link token.

        Args:
            user_id (str): User identifier.

        Returns:
            dict or None: Link token response or None if creation fails.
        """
        try:
            response = cls.plaid_integration.create_link_token(user_id)
            logger.info(f"Plaid link token created: {response}")
            return response
        except Exception as e:
            logger.error(f"Error creating Plaid link token: {e}")
            return None

    @classmethod
    def exchange_plaid_public_token(cls, public_token):
        """
        Exchange a Plaid public token for an access token.

        Args:
            public_token (str): Public token.

        Returns:
            dict or None: Access token response or None if exchange fails.
        """
        try:
            response = cls.plaid_integration.exchange_public_token(public_token)
            logger.info(f"Plaid public token exchanged: {response}")
            return response
        except Exception as e:
            logger.error(f"Error exchanging Plaid public token: {e}")
            return None

    @classmethod
    def get_plaid_accounts(cls, access_token):
        """
        Retrieve Plaid accounts linked to the access token.

        Args:
            access_token (str): Access token.

        Returns:
            dict or None: Accounts information or None if retrieval fails.
        """
        try:
            response = cls.plaid_integration.get_accounts(access_token)
            logger.info(f"Plaid accounts retrieved: {response}")
            return response
        except Exception as e:
            logger.error(f"Error retrieving Plaid accounts: {e}")
            return None


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
    ach_response = bank_utils.create_ach_payment(account, routing, 100.0, "Test ACH payment")
    print(f"ACH Payment Response: {ach_response}")

    # Plaid example (requires valid tokens)
    user_id = "user123"
    link_token_response = bank_utils.create_plaid_link_token(user_id)
    print(f"Plaid Link Token Response: {link_token_response}")
