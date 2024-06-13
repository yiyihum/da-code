from sympy import symbols, Eq, solve, Abs, Piecewise
import pandas as pd

# Define the variables
x, y = symbols('x y', real=True)

# Define the objective function
objective_function = 5*x**2 + 5*y**2 - 8*x*y

# Define the constraint involving absolute values
constraint = Eq(Abs(x - 2*y) + Abs(y - 2*x), 40)

# List to store minimum values for each case
min_values = []

# There are four cases to consider based on the properties of absolute values
cases = [
    {'cond': [x - 2*y >= 0, y - 2*x >= 0]},
    {'cond': [x - 2*y >= 0, y - 2*x < 0]},
    {'cond': [x - 2*y < 0, y - 2*x >= 0]},
    {'cond': [x - 2*y < 0, y - 2*x < 0]}
]

# Solve each case
for case in cases:
    # Create the new constraint for the current case
    new_constraint = constraint.subs({
        Abs(x - 2*y): Piecewise((x - 2*y, case['cond'][0]), (-x + 2*y, True)),
        Abs(y - 2*x): Piecewise((y - 2*x, case['cond'][1]), (-y + 2*x, True))
    })

    # Solve the new constraint for x and y
    solutions = solve(new_constraint, (x, y), dict=True)

    # Calculate the objective function for each solution and find the minimum
    for sol in solutions:
        # Check if the solution is valid (i.e., it satisfies all original conditions)
        if all(cond.subs(sol) for cond in case['cond']):
            value = objective_function.subs(sol)
            min_values.append(value)

# Check if min_values is not empty and find the minimum value
if min_values:
    min_value = min(min_values)
else:
    min_value = None

# Output the minimum value
print(f"The minimum value of the expression is: {min_value}")

# Write the result into result.csv
result_df = pd.DataFrame({'id': ['430b63'], 'result': [min_value]})
result_df.to_csv('result.csv', index=False)
