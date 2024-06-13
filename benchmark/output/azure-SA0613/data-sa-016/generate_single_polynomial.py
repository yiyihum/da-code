import sympy as sp

# Function to generate the Poincare polynomial for SU(m)
def poincare_polynomial(m):
    t = sp.symbols('t')
    polynomial = 1
    for i in range(1, m + 1):
        polynomial *= (1 + t**(2*i + 1)**2)
    return polynomial.expand()

# Generate the polynomial for m=10 and extract coefficients
m = 10
polynomial = poincare_polynomial(m)
coeffs = polynomial.as_coefficients_dict()

# Extract degrees and coefficients without simplification
degrees = []
coefficients = []
for exp, coeff in coeffs.items():
    # Ensure that the exponent is a pure integer
    if exp.is_Integer:
        degrees.append(int(exp))
        coefficients.append(int(coeff))

# Output the degrees and coefficients to verify
print("Degrees:", degrees)
print("Coefficients:", coefficients)
