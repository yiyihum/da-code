from sympy import *

# Define symbols
x, y = symbols('x y', real=True)

# Define the objective function
f = 5*x**2 + 5*y**2 - 8*x*y

# Use the constraint to eliminate one variable
eq = Eq(abs(x - 2*y) + abs(y - 2*x), 40)
y_sol = solve(eq, y)

# Substitute the solution into the objective function
f_x = f.subs(y, y_sol[0])

# Find the critical points
df_dx = diff(f_x, x)
critical_points = solve(df_dx)

# Evaluate the objective function at the critical points and the boundary points
min_val = f_x.subs(x, critical_points[0])
for i in range(1, len(critical_points)):
    min_val = min(min_val, f_x.subs(x, critical_points[i]))

# Print the minimum value
print(min_val)