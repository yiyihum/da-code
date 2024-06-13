import sympy as sp

# Define the variable and function
x = sp.symbols('x')
f = x**3 - 6*x**2 + 9*x + 15

# Calculate the first and second derivatives
f_prime = sp.diff(f, x)
f_double_prime = sp.diff(f_prime, x)

# Find the critical points by solving f'(x) = 0
critical_points = sp.solve(f_prime, x)

# Determine the nature of each critical point
turning_points = []
for point in critical_points:
    second_derivative_value = f_double_prime.subs(x, point)
    if second_derivative_value > 0:
        nature = "minimum"
    elif second_derivative_value < 0:
        nature = "maximum"
    else:
        nature = "point of inflection"
    turning_points.append((point, nature))

# Write the results to a CSV file
import csv

with open('/workspace/turning_points.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['x', 'nature'])
    for point, nature in turning_points:
        writer.writerow([point, nature])
