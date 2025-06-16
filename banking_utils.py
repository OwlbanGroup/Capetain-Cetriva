import logging
from generate_account_number import generate_account_number, is_valid_account_number
from get_routing_number import get_routing_number
from validate_routing_number import validate_routing_number


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BankingUtils:
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
