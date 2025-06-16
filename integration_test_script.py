from banking_utils import BankingUtils


def integration_test():
    bank_utils = BankingUtils()

    # Test account number generation
    try:
        account_number = bank_utils.generate_account(10)
        assert account_number is not None and len(account_number) == 10, "Account number generation failed"
        print(f"Generated Account Number: {account_number}")
    except Exception as e:
        print(f"Account number generation test failed: {e}")

    # Test routing number retrieval
    bank_name = "Capetain Cetriva"
    try:
        routing_number = bank_utils.get_routing(bank_name)
        assert routing_number is not None and len(routing_number) > 0, "Routing number retrieval failed"
        print(f"Routing Number for {bank_name}: {routing_number}")
    except Exception as e:
        print(f"Routing number retrieval test failed: {e}")
        routing_number = None

    # Test routing number validation
    if routing_number:
        try:
            is_valid = bank_utils.validate_routing(routing_number)
            assert isinstance(is_valid, bool), "Routing number validation did not return a boolean"
            print(f"Is Routing Number Valid? {is_valid}")
        except Exception as e:
            print(f"Routing number validation test failed: {e}")
    else:
        print("No routing number retrieved to validate.")


if __name__ == "__main__":
    integration_test()
