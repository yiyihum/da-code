import sympy as sp

# Define the symbol 't' globally
t = sp.symbols('t')

# Define the polynomial function
def generate_polynomial(m):
    polynomial = 1
    for i in range(1, m + 1):
        polynomial *= (1 + t ** ((2 * i + 1) ** 3))
    return polynomial

# Test polynomial generation and coefficient extraction for a single degree
degree = 10
polynomial = generate_polynomial(degree)
coeffs = polynomial.expand().as_ordered_terms()
coefficients = [float(sp.Poly(term, t).coeffs()[0]) for term in coeffs if t in sp.Poly(term, t).gens]

# Output the first few coefficients to verify the process
print(coefficients[:5])
