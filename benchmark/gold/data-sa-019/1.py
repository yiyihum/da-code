import sympy as sp
import pandas as pd

# Read the generated CSV file
df = pd.read_csv('../cubic_function.csv')

# Defining the symbol for differentiation
x = sp.symbols('x')

# Define the cubic function
y = x**3 - 6*x**2 + 9*x + 15

# Calculating the first derivative
first_derivative = sp.diff(y, x)

# Finding the critical points (where the first derivative is zero)
critical_points = sp.solve(first_derivative, x)

# Calculating the second derivative
second_derivative = sp.diff(first_derivative, x)

# Analyzing the nature of each critical point and finding their y-coordinates
turning_points = []
for cp in critical_points:
    second_derivative_value = second_derivative.subs(x, cp)
    y_value = y.subs(x, cp)
    if second_derivative_value > 0:
        nature = "Minimum"
    elif second_derivative_value < 0:
        nature = "Maximum"
    else:
        nature = "Point of Inflection"
    turning_points.append((float(cp), float(y_value), nature))

# Verify the results with the CSV data
df['Nature'] = df.apply(
    lambda row: 'Minimum' if row['x'] == 3.0 else ('Maximum' if row['x'] == 1.0 else 'None'), axis=1
)

# Create a DataFrame for turning points and save to CSV
turning_points_df = pd.DataFrame(turning_points, columns=['Critical Point (x)', 'Function Value (y)', 'Nature'])
turning_points_df.to_csv('./turning_points.csv', index=False)


