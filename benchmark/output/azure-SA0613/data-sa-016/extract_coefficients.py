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

# Extract degrees and coefficients
coeffs = polynomial.as_coefficients_dict()
sorted_coeffs = sorted(coeffs.items(), key=lambda x: sp.degree(x[0]))

# Output the sorted degrees and coefficients to verify
for term, coeff in sorted_coeffs:
    degree = sp.degree(term)
    print(f'Degree: {degree}, Coefficient: {coeff}')
