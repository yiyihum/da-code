# Problem 2: Optimizing Cylinder Dimensions
# In this problem, we are given a fixed surface area S=100 sq units  
# and need to determine the dimensions 
# (radius r and height h of a right circular cylinder that will maximize its volume)

# Importing the necessary libraries
import sympy as sp
import pandas as pd

# Defining the symbols for radius (r) and height (h)
r, h = sp.symbols('r h')

# Given surface area (example: 100 units^2)
surface_area = 100

# Surface area formula for a cylinder: 2*pi*r*h + 2*pi*r^2
# Using the surface area to express h in terms of r
h_expr = (surface_area - 2*sp.pi*r**2) / (2*sp.pi*r)

# Volume of a cylinder: pi*r^2*h
# Substitute h from the surface area constraint
volume = sp.pi * r**2 * h_expr

# Differentiate the volume w.r.t r to find the critical point for maximum volume
dv_dr = sp.diff(volume, r)

# Solve the equation dv_dr = 0 to find the optimal radius
optimal_radius_solutions = sp.solve(dv_dr, r)

# Display all solutions
all_solutions = [(rad, h_expr.subs(r, rad)) for rad in optimal_radius_solutions]

# Explanation for discarding negative values
# Filtering only positive real solutions for radius and height
optimal_dimensions = [(rad.evalf(), h_val.evalf()) for rad, h_val in all_solutions if rad.is_real and rad > 0 and h_val.is_real and h_val > 0]

# Calculating the maximum volume
if optimal_dimensions:
    radius, height = optimal_dimensions[0]
    max_volume = sp.pi * radius**2 * height
    max_volume_value = max_volume.evalf()
    optimal_dimensions_with_volume = [(radius, height, max_volume_value)]
else:
    optimal_dimensions_with_volume = [("No valid physical solution found", "", "")]

# Creating a DataFrame and saving to CSV
columns = ['Optimal Radius (r)', 'Optimal Height (h)', 'Maximum Volume']
df = pd.DataFrame(optimal_dimensions_with_volume, columns=columns)
df.to_csv('optimal_cylinder_dimensions.csv', index=False)

# Display the DataFrame
print(df)
