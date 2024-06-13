import numpy as np

# Define the function to check the number of solutions for a given m
def number_of_solutions(m):
    # Define the equation as a lambda function
    equation = lambda x: abs(abs(x - 1) - 2) - m / 100
    # Use a large range of x values to find potential solutions
    x_values = np.linspace(-10, 10, 10000)
    # Check where the equation crosses zero, which indicates a solution
    solutions = np.where(np.diff(np.sign(equation(x_values))))[0]
    return len(solutions)

# Check for each m from 1 to 10000 (since m/100 must be an integer, m is at most 10000)
results = []
for m in range(1, 10001):
    if number_of_solutions(m) == 4:
        results.append(m)

# Write the result to a CSV file
with open('/workspace/result.csv', 'w') as file:
    file.write('id,answer\n')
    file.write('739bc9,' + str(len(results)) + '\n')

print("The number of positive integers m for which the equation has 4 distinct solutions is:", len(results))
