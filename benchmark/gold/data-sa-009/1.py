from sympy import *

points = []

for x in range(-100, 100):
    for y in range(-100, 100):
        if ((abs(x + y)-10)**2 + (abs(x - y)-10)**2) * ((abs(x)-8)**2 + (abs(y)-8)**2) == 0:
            points.append(Point(x, y))

# Find the convex hull
hull = convex_hull(*points)

# Create a Polygon object from the convex hull vertices
polygon = Polygon(*hull.vertices)

# Calculate the area of the polygon
area = polygon.area

# Print the area
print(area)
