from sympy import *

# Define symbols
total_outcomes = 6**4
successful_outcomes = 0

# Iterate over all possible outcomes
for die1 in range(1, 7):
    for die2 in range(1, 7):
        for die3 in range(1, 7):
            for die4 in range(1, 7):
                # Check if the highest roll is a 5
                if max(die1, die2, die3, die4) == 5:
                    successful_outcomes += 1

# Calculate the probability
probability = Rational(successful_outcomes, total_outcomes)

# Get the numerator (a) and denominator (b) of the probability
a = probability.p
b = probability.q

# Print the sum of a and b
print(a + b)
