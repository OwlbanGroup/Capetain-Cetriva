import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_routing_number(routing_number):
    """
    Validates a US bank routing number using the checksum algorithm.
    Routing number must be a 9-digit string.
    Returns True if valid, False otherwise.
    """
    if not isinstance(routing_number, str):
        logger.error("Routing number must be a string")
        return False

    if len(routing_number) != 9 or not routing_number.isdigit():
        logger.error("Routing number must be a 9-digit string")
        return False

    digits = list(map(int, routing_number))
    checksum = (
        3 * (digits[0] + digits[3] + digits[6]) +
        7 * (digits[1] + digits[4] + digits[7]) +
        1 * (digits[2] + digits[5] + digits[8])
    )
    is_valid = checksum % 10 == 0
    logger.info(
        f"Routing number {routing_number} validation result: {is_valid}"
    )
    return is_valid


if __name__ == "__main__":
    routing_number = "987654321"
    is_valid = validate_routing_number(routing_number)
    print(f"Routing number {routing_number} is {'valid' if is_valid else 'invalid'}.")
