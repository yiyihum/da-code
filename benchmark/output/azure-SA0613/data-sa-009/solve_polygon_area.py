import numpy as np
import pandas as pd

# The equations can be simplified by considering the cases for the absolute values.
# We can break down the equations into four cases for each quadrant.

# Define the line segments for each quadrant
segments = [
    [(10, 0), (0, 10)],  # Segment in the first quadrant for eq1
    [(8, 0), (0, 8)],    # Segment in the first quadrant for eq2
    [(-10, 0), (0, 10)], # Segment in the second quadrant for eq1
    [(-8, 0), (0, 8)],   # Segment in the second quadrant for eq2
    [(-10, 0), (0, -10)],# Segment in the third quadrant for eq1
    [(-8, 0), (0, -8)],  # Segment in the third quadrant for eq2
    [(10, 0), (0, -10)], # Segment in the fourth quadrant for eq1
    [(8, 0), (0, -8)]    # Segment in the fourth quadrant for eq2
]

# Calculate the intersection of two line segments
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

# Find all intersections between the line segments
vertices = []
for i in range(len(segments)):
    for j in range(i+1, len(segments)):
        try:
            intersect = line_intersection(segments[i], segments[j])
            # Check if the intersection is within the segment bounds
            if all(min(a) <= b <= max(a) for a, b in zip(segments[i], intersect)) and                all(min(a) <= b <= max(a) for a, b in zip(segments[j], intersect)):
                vertices.append(intersect)
        except:
            pass

# Remove duplicates and sort the vertices in counterclockwise order
vertices = list(set(vertices))
vertices.sort(key=lambda v: np.arctan2(v[1], v[0]))

# Calculate the area of the convex polygon using the shoelace formula
def polygon_area(vertices):
    n = len(vertices)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    area = abs(area) / 2.0
    return area

# Calculate the area
area = polygon_area(vertices)

# Write the result to result.csv
result_df = pd.DataFrame({'id': ['8ee6f3'], 'area': [area]})
result_df.to_csv('result.csv', index=False)

print(f"The area of the convex polygon is: {area}")
