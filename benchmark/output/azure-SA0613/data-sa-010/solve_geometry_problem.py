import sympy as sp

# Define the points based on the problem statement
A = sp.Point(0, 0)
B = sp.Point(1, 0)
C = sp.Point(1, 1)
D = sp.Point(0, 1)
P = sp.Point(1/20, 0)
Q = sp.Point(0, 1/24)

# Define the lines DP and BQ
DP = sp.Line(D, P)
BQ = sp.Line(B, Q)

# Find the intersection of lines DP and BQ
R = DP.intersection(BQ)[0]

# Calculate the areas of the triangles and the quadrilateral
triangle_APD = sp.Polygon(A, P, D)
triangle_BQC = sp.Polygon(B, Q, C)
triangle_RPB = sp.Polygon(R, P, B)
triangle_RQD = sp.Polygon(R, Q, D)
quadrilateral_ARQC = sp.Polygon(A, R, Q, C)

# Calculate the areas
area_APD = abs(triangle_APD.area)
area_BQC = abs(triangle_BQC.area)
area_RPB = abs(triangle_RPB.area)
area_RQD = abs(triangle_RQD.area)
area_ARQC = abs(quadrilateral_ARQC.area)

# Calculate the ratio of the largest to the smallest area
areas = [area_APD, area_BQC, area_RPB, area_RQD, area_ARQC]
ratio = max(areas) / min(areas)

# Write the result to result.csv
with open('result.csv', 'w') as file:
    file.write(f'bedda4,{float(ratio)}\n')
