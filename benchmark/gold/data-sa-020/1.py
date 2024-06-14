import csv
import math

# Function to calculate the optimal radius and height for a given surface area
def calculate_optimal_dimensions(area):
    # Given the formula for surface area S = 2 * pi * r * (r + h) and h = 2 * r,
    # we can solve for r: S = 2 * pi * r * (r + 2 * r) = 2 * pi * r * (3 * r)
    # => r = sqrt(S / (6 * pi))
    r = math.sqrt(area / (6 * math.pi))
    h = 2 * r
    volume = math.pi * r**2 * h
    return r, h, volume

# Read the CSV file and calculate the optimal dimensions
with open('optimal_cylinder_dimensions.csv', mode='r') as infile:
    reader = csv.reader(infile)
    data = list(reader)

# Skip the header row and calculate dimensions for each area value
results = [data[0]]  # Include the header
for row in data[1:]:
    area = float(row[0])
    r, h, volume = calculate_optimal_dimensions(area)
    results.append([area, r, h, volume])

# Write the results back to the CSV file
with open('optimal_cylinder_dimensions.csv', mode='w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(results)
