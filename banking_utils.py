import logging
from generate_account_number import generate_account_number, is_valid_account_number
from get_routing_number import get_routing_number
from validate_routing_number import validate_routing_number
from ach_payments import ACHPayments
from plaid_integration import PlaidIntegration


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BankingUtils:
    ach_payments = ACHPayments()
    plaid_integration = PlaidIntegration()

    @staticmethod
    def generate_account(length=9):
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
        try:
            routing_number = get_routing_number(bank_name)
            logger.info(f"Retrieved routing number for {bank_name}: {routing_number}")
            return routing_number
        except Exception as e:
            logger.error(f"Error retrieving routing number for {bank_name}: {e}")
            return None

    @staticmethod
    def validate_routing(routing_number):
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
        try:
            response = cls.ach_payments.create_payment(
                account_number, routing_number, amount, description
            )
            logger.info(f"ACH payment created: {response}")
            return response
        except Exception as e:
            logger.error(f"Error creating ACH payment: {e}")
            return None

    @classmethod
    def get_ach_payment_status(cls, transaction_id):
        try:
            status = cls.ach_payments.get_payment_status(transaction_id)
            logger.info(f"ACH payment status: {status}")
            return status
        except Exception as e:
            logger.error(f"Error getting ACH payment status: {e}")
            return None

    @classmethod
    def create_plaid_link_token(cls, user_id):
        try:
            response = cls.plaid_integration.create_link_token(user_id)
            logger.info(f"Plaid link token created: {response}")
            return response
        except Exception as e:
            logger.error(f"Error creating Plaid link token: {e}")
            return None

    @classmethod
    def exchange_plaid_public_token(cls, public_token):
        try:
            response = cls.plaid_integration.exchange_public_token(public_token)
            logger.info(f"Plaid public token exchanged: {response}")
            return response
        except Exception as e:
            logger.error(f"Error exchanging Plaid public token: {e}")
            return None

    @classmethod
    def get_plaid_accounts(cls, access_token):
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
