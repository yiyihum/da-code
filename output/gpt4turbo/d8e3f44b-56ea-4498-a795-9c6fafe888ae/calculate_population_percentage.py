import json

# Given data for Algeria
P_0 = 44903225  # Population in 2022
r = 1.0164  # Growth rate
current_world_percentage = 0.56  # World population percentage in 2022

# Function to calculate future population using the provided formula
def calculate_future_population(P_0, r, t):
    return P_0 * ((1 + r / 100) ** t)

# Function to calculate future world population percentage
def calculate_percentage(P_t, current_world_percentage):
    return (P_t / P_0) * current_world_percentage

# Calculate population for the years 2030, 2040, and 2050
P_2030 = calculate_future_population(P_0, r, 2030 - 2022)
P_2040 = calculate_future_population(P_0, r, 2040 - 2022)
P_2050 = calculate_future_population(P_0, r, 2050 - 2022)

# Calculate world population percentage for the years 2030, 2040, and 2050
percentage_2030 = calculate_percentage(P_2030, current_world_percentage)
percentage_2040 = calculate_percentage(P_2040, current_world_percentage)
percentage_2050 = calculate_percentage(P_2050, current_world_percentage)

# Prepare the result in JSON format
result = {
    "Algeria 2030 World Population Percentage": [percentage_2030],
    "Algeria 2040 World Population Percentage": [percentage_2040],
    "Algeria 2050 World Population Percentage": [percentage_2050]
}

# Output the result
print(json.dumps(result, indent=2))
