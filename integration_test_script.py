from banking_utils import BankingUtils


def integration_test():
    bank_utils = BankingUtils()

    # Test account number generation
    account_number = bank_utils.generate_account(10)
    print(f"Generated Account Number: {account_number}")

    # Test routing number retrieval
    bank_name = "Capetain Cetriva"
    routing_number = bank_utils.get_routing(bank_name)
    print(f"Routing Number for {bank_name}: {routing_number}")

    # Test routing number validation
    if routing_number:
        is_valid = bank_utils.validate_routing(routing_number)
        print(f"Is Routing Number Valid? {is_valid}")
    else:
        print("No routing number retrieved to validate.")


if __name__ == "__main__":
    integration_test()
