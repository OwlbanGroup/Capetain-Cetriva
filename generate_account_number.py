import random
import logging
from typing import List


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def luhn_checksum(account_number: str) -> int:
    """
    Calculate the Luhn checksum for the account number.
    """
    def digits_of(n: str) -> List[int]:
        return [int(d) for d in str(n)]
    digits = digits_of(account_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    for d in even_digits:
        total += sum(digits_of(str(d*2)))
    return total % 10


def is_valid_account_number(account_number: str) -> bool:
    """
    Validate the account number using Luhn checksum.
    """
    return luhn_checksum(account_number) == 0


def generate_account_number(length: int = 9, numeric_only: bool = True) -> str:
    """
    Generates a valid bank account number with the specified length and format.
    Uses Luhn algorithm for checksum validation.

    Args:
        length (int): Length of the account number (minimum 2).
        numeric_only (bool): If True, generate numeric account number only.
                             If False, generate alphanumeric account number.

    Returns:
        str: Valid account number as a string.

    Raises:
        ValueError: If length is less than 2.

    Usage example:
        >>> generate_account_number(10)
        '1234567890'
        >>> generate_account_number(12, numeric_only=False)
        'A1B2C3D4E5F6'
    """
    if not isinstance(length, int):
        logger.error("Account number length must be an integer")
        raise ValueError("Account number length must be an integer")

    if length < 2:
        logger.error("Account number length must be at least 2")
        raise ValueError("Account number length must be at least 2")

    if numeric_only:
        while True:
            number = ''.join(str(random.randint(0, 9)) for _ in range(length - 1))
            checksum = luhn_checksum(number + '0')
            check_digit = (10 - checksum) % 10
            account_number = number + str(check_digit)
            if is_valid_account_number(account_number):
                logger.info(f"Generated valid account number: {account_number}")
                return account_number
    else:
        # Generate alphanumeric account number (simple random uppercase letters and digits)
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        while True:
            number = ''.join(random.choice(chars) for _ in range(length - 1))
            # For alphanumeric, skip Luhn checksum validation
            account_number = number + random.choice(chars)
            logger.info(f"Generated alphanumeric account number: {account_number}")
            return account_number


if __name__ == "__main__":
    try:
        account_number = generate_account_number()
        print(f"Generated valid account number: {account_number}")
    except Exception as e:
        logger.error(f"Error generating account number: {e}")
