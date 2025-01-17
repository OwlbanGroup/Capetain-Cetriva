from fund_in_a_box import stay_in_your_home_program

# Sample parameters for testing
income = 45000
home_value = 250000
loan_amount = 200000
assistance_needed = 30000

# Call the function and assert the result
assistance = stay_in_your_home_program(income, home_value, loan_amount, assistance_needed)
print(f"Assistance amount: ${assistance}")
assert assistance == 30000  # Expected assistance based on the parameters

# Additional test cases
# Test case 1: Edge case with zero income
income = 0
assistance = stay_in_your_home_program(income, home_value, loan_amount, assistance_needed)
print(f"Assistance amount with zero income: ${assistance}")
assert assistance == 0  # Expected assistance is 0

# Test case 2: High home value
home_value = 1000000
assistance = stay_in_your_home_program(income, home_value, loan_amount, assistance_needed)
print(f"Assistance amount with high home value: ${assistance}")
assert assistance == 0  # Expected assistance is 0

# Test case 3: Loan amount greater than home value
loan_amount = 300000
assistance = stay_in_your_home_program(income, home_value, loan_amount, assistance_needed)
print(f"Assistance amount with loan greater than home value: ${assistance}")
assert assistance == 0  # Expected assistance is 0
