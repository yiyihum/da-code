import numpy as np
from scipy.optimize import minimize
import pandas as pd

# Define the objective function
def objective_function(vars):
    x, y = vars
    return 5*x**2 + 5*y**2 - 8*x*y

# Define the constraint function
def constraint_function(vars):
    x, y = vars
    return np.abs(x - 2*y) + np.abs(y - 2*x) - 40

# Initial guess (a valid point that satisfies the constraint)
x0 = [10, 15]

# Define the constraint in the form required by scipy.optimize.minimize
cons = ({'type': 'eq', 'fun': constraint_function})

# Perform the minimization
result = minimize(objective_function, x0, constraints=cons, method='SLSQP')

# The minimum value of the objective function
min_value = result.fun if result.success else None

# Output the minimum value
print(f"The minimum value of the expression is: {min_value}")

# Write the result into result.csv
result_df = pd.DataFrame({'id': ['430b63'], 'result': [min_value]})
result_df.to_csv('result.csv', index=False)
