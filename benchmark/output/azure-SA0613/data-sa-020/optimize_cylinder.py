import scipy.optimize as opt
import numpy as np

# Fixed surface area
S = 100

# Function to calculate the height of the cylinder given its radius and fixed surface area
def height(r, S):
    return S / (2 * np.pi * r) - r

# Function to calculate the volume of the cylinder
def volume(r, S):
    h = height(r, S)
    return np.pi * r**2 * h

# Function to calculate the negative volume, since we will be using a minimization function
def negative_volume(r, S):
    return -volume(r, S)

# Initial guess for the radius
initial_guess = [1]

# Bounds for the radius, it must be positive and less than sqrt(S/(2*pi)) to have a real height
radius_bounds = [(0, np.sqrt(S / (2 * np.pi)))]

# Perform the optimization to maximize the volume (minimize the negative volume)
result = opt.minimize(negative_volume, initial_guess, args=(S), bounds=radius_bounds)

# Calculate the optimized radius and height
optimized_radius = result.x[0]
optimized_height = height(optimized_radius, S)

# Print the results
print(f"Optimized radius: {optimized_radius}")
print(f"Optimized height: {optimized_height}")
print(f"Maximized volume: {volume(optimized_radius, S)}")
