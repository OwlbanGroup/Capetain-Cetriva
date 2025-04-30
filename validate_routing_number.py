def validate_routing_number(routing_number):
    """
    Validates a US bank routing number using the checksum algorithm.
    Routing number must be a 9-digit string.
    Returns True if valid, False otherwise.
    """
    if len(routing_number) != 9 or not routing_number.isdigit():
        return False

    digits = list(map(int, routing_number))
    checksum = (
        3 * (digits[0] + digits[3] + digits[6]) +
        7 * (digits[1] + digits[4] + digits[7]) +
        1 * (digits[2] + digits[5] + digits[8])
    )
    return checksum % 10 == 0

if __name__ == "__main__":
    routing_number = "987654321"
    is_valid = validate_routing_number(routing_number)
    print(f"Routing number {routing_number} is {'valid' if is_valid else 'invalid'}.")
