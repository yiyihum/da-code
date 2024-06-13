import sympy as sp

# Function to generate the Poincare polynomial for SU(m)
def poincare_polynomial(m):
    t = sp.symbols('t')
    polynomial = 1
    for i in range(1, m + 1):
        polynomial *= (1 + t**(2*i + 1)**2)
    return polynomial.expand()

# Generate the polynomial for m=15 and extract coefficients
m = 15
polynomial = poincare_polynomial(m)
coeffs = polynomial.as_coefficients_dict()

# Extract degrees and coefficients
coefficients_m15 = [(int(sp.degree(term)), int(coeff)) for term, coeff in coeffs.items()]

# Output the sorted degrees and coefficients to verify
sorted_coeffs_m15 = sorted(coefficients_m15, key=lambda x: x[0])
print(f"m={m}:")
for degree, coeff in sorted_coeffs_m15:
    print(f'Degree: {degree}, Coefficient: {coeff}')
