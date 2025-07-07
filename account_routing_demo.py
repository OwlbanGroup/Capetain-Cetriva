from banking_utils import BankingUtils


def main():
    bank_utils = BankingUtils()

    # Generate a valid account number
    account_number = bank_utils.generate_account(10)
    print(f"Generated Account Number: {account_number}")

    # Retrieve routing number for the project bank
    bank_name = "Capetain Cetriva"
    routing_number = bank_utils.get_routing(bank_name)
    print(f"Routing Number for {bank_name}: {routing_number}")

    # Validate the retrieved routing number
    if routing_number:
        is_valid = bank_utils.validate_routing(routing_number)
        print(f"Is Routing Number Valid? {is_valid}")
    else:
        print("Failed to retrieve routing number.")


if __name__ == "__main__":
    main()

