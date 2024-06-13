from sympy import *

# Points
A = Point(0, 0)
B = Point(1, 0)
C = Point(1, 1)
D = Point(0, 1)
P = Point(Rational(1,20), 0)
Q = Point(0, Rational(1,24))

# Lines
line_DP = Line(D, P)
line_BQ = Line(B, Q)

# Intersection
intersection = line_DP.intersection(line_BQ)[0]

# Areas
# Region 1: Quadrilateral A, P, Intersection, Q
area1 = Polygon(A, P, intersection, Q).area

# Region 2: P, B, Intersection
area2 = Polygon(P, B, intersection).area

# Region 3: B, C, D, Intersection
area3 = Polygon(B, C, D, intersection).area

# Region 4: D, Q, Intersection
area4 = Polygon(D, Q, intersection).area

ratio = max([area1, area2, area3, area4]) / min([area1, area2, area3, area4])
print(ratio)
