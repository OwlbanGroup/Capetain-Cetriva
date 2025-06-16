import random
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def luhn_checksum(account_number):
    """
    Calculate the Luhn checksum for the account number.
    """
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(account_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    for d in even_digits:
        total += sum(digits_of(d*2))
    return total % 10


def is_valid_account_number(account_number):
    """
    Validate the account number using Luhn checksum.
    """
    return luhn_checksum(account_number) == 0


def generate_account_number(length=9):
    """
    Generates a valid bank account number with the specified length.
    Uses Luhn algorithm for checksum validation.
    Args:
        length (int): Length of the account number (minimum 2).
    Returns:
        str: Valid account number as a string.
    Raises:
        ValueError: If length is less than 2.
    """
    if length < 2:
        logger.error("Account number length must be at least 2")
        raise ValueError("Account number length must be at least 2")

    while True:
        number = ''.join(str(random.randint(0, 9)) for _ in range(length - 1))
        checksum = luhn_checksum(number + '0')
        check_digit = (10 - checksum) % 10
        account_number = number + str(check_digit)
        if is_valid_account_number(account_number):
            logger.info(f"Generated valid account number: {account_number}")
            return account_number


if __name__ == "__main__":
    account_number = generate_account_number()
    print(f"Generated valid account number: {account_number}")
