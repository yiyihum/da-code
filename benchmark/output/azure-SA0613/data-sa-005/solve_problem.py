import sympy as sp

# Define the symbols
k, l, x = sp.symbols('k l x')

# Define the equation of the parabola and the line
parabola_eq = k * x**2 - 2 * k * x + l
line_y = 4

# Solve for x where the parabola intersects the line y = 4
intersection_xs = sp.solve(parabola_eq - line_y, x)

# We expect two x values for the points of intersection
assert len(intersection_xs) == 2, "There should be two x values for intersection points."

# The distance between the points A and B is 6
# Since the y-coordinate is the same for both points (y = 4), we only consider the x-coordinate
# We square the distance equation to avoid dealing with the absolute value and square root
distance_eq = sp.Eq((intersection_xs[0] - intersection_xs[1])**2, 36)

# Solve for k and l using the distance equation and the parabola equation at one of the x values
solutions = sp.solve([distance_eq, parabola_eq.subs(x, intersection_xs[0]) - line_y], (k, l))

# Check if we got a solution
if not solutions:
    print("No solution found for k and l.")
else:
    # Extract the solutions for k and l
    k_value, l_value = solutions[0]

    # Substitute k and l into the x-coordinates of A and B
    A_x_value = intersection_xs[0].subs({k: k_value, l: l_value}).evalf()
    B_x_value = intersection_xs[1].subs({k: k_value, l: l_value}).evalf()

    # The y-coordinate is 4 for both A and B
    A_y_value = B_y_value = line_y

    # Calculate the sum of the squares of the distances from A and B to the origin
    sum_of_squares = A_x_value**2 + A_y_value**2 + B_x_value**2 + B_y_value**2

    # Substitute the value of k into the sum_of_squares expression to get a numerical result
    numerical_result = sum_of_squares.subs(k, k_value).evalf()

    # Output the result
    print(f"The sum of the squares of the distances from A and B to the origin is: {numerical_result}")

    # Write the result to result.csv
    with open('result.csv', 'w') as file:
        file.write('id,answer\n')
        file.write(f'229ee8,{numerical_result}\n')
