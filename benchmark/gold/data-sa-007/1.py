from sympy import *

# Define symbols
x = Symbol('x', real=True)
m = Symbol('m', integer=True, positive=True)

# Define the equation
eq = Eq(abs(abs(x - 1) - 2), m/100)

# Initialize a counter for the number of valid m values
valid_m_count = 0

# Iterate over possible m values from -1000 to 1000
for m_val in range(-1000, 1000+1):
    # Substitute the current m value into the equation
    curr_eq = eq.subs(m, m_val)

    # Solve the equation for the current m value
    solutions = solveset(curr_eq, x, domain=Reals)

    # Check if the solution set is a FiniteSet (indicating distinct solutions)
    if isinstance(solutions, FiniteSet):
        # Check if there are exactly 4 distinct real solutions
        if len(solutions) == 4:
            valid_m_count += 1

print(valid_m_count)
