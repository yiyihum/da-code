import sympy as sp

# Function to generate the Poincare polynomial for SU(m)
def poincare_polynomial(m):
    t = sp.symbols('t')
    polynomial = 1
    for i in range(1, m + 1):
        polynomial *= (1 + t**(2*i + 1)**2)
    return polynomial.expand()

# Generate the polynomial for m=10
m = 10
polynomial = poincare_polynomial(m)

# Print the polynomial to verify its correctness
print("Polynomial for m=10:", polynomial)
