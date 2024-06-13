from math import gcd
from fractions import Fraction

# Function to calculate the greatest common divisor (gcd)
def calculate_gcd(x, y):
    return gcd(x, y)

# Function to calculate the probability that the highest roll is a 5
def probability_highest_five():
    # Total possible outcomes for four 6-sided dice
    total_outcomes = 6**4
    
    # Outcomes where the highest roll is at most 5 (all dice show 5 or less)
    at_most_5_outcomes = 5**4
    
    # Outcomes where the highest roll is at most 4 (all dice show 4 or less)
    at_most_4_outcomes = 4**4
    
    # Probability that the highest roll is exactly 5
    # is the difference between at most 5 and at most 4 outcomes
    exact_5_outcomes = at_most_5_outcomes - at_most_4_outcomes
    
    # Calculate the probability as a fraction
    probability = Fraction(exact_5_outcomes, total_outcomes)
    
    # Simplify the fraction
    gcd_value = calculate_gcd(probability.numerator, probability.denominator)
    simplified_numerator = probability.numerator // gcd_value
    simplified_denominator = probability.denominator // gcd_value
    
    # Return the sum of the numerator and denominator of the simplified fraction
    return simplified_numerator + simplified_denominator

# Calculate the result
result = probability_highest_five()

# Write the result to result.csv
with open('result.csv', 'w') as file:
    file.write('id,result\n')  # Write the header
    file.write(f'82e2a0,{result}\n')  # Write the problem ID and result

print(f'Result written to result.csv: 82e2a0,{result}')
