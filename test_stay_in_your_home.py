# test_stay_in_your_home.py
from fund_in_a_box import stay_in_your_home_program

# Sample parameters for testing
income = 45000
home_value = 250000
loan_amount = 200000
assistance_needed = 30000

# Call the function and print the result
assistance = stay_in_your_home_program(income, home_value, loan_amount, assistance_needed)
print(f"Assistance amount: ${assistance}")
