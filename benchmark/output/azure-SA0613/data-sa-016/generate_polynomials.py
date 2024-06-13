import sympy as sp
import numpy as np
from scipy.stats import norm

# Function to generate the Poincare polynomial for SU(m)
def poincare_polynomial(m):
    t = sp.symbols('t')
    polynomial = 1
    for i in range(1, m + 1):
        polynomial *= (1 + t**(2*i + 1)**2)
    return polynomial.expand()

# Function to fit the coefficients to a normal distribution and write to CSV
def fit_and_write_to_csv(m, file_name):
    # Generate the polynomial and get the coefficients
    polynomial = poincare_polynomial(m)
    coeffs = polynomial.as_coefficients_dict()

    # Extract degrees and coefficients
    degrees = []
    coefficients = []
    for exp, coeff in coeffs.items():
        # Ensure that the exponent is a pure integer
        if isinstance(exp, sp.Integer):
            degrees.append(int(exp))
            coefficients.append(int(coeff))

    # Sort the degrees and coefficients together
    sorted_degrees, sorted_coefficients = zip(*sorted(zip(degrees, coefficients)))

    # Fit the coefficients to a normal distribution
    mu, std = norm.fit(sorted_coefficients)

    # Calculate the fitted normal PDF values
    fitted_normal_pdf = norm.pdf(sorted_degrees, mu, std)

    # Write to CSV
    with open(file_name, 'w') as file:
        file.write('Degree,Coefficient,Fitted_Normal_PDF\n')
        for degree, coeff, pdf_value in zip(sorted_degrees, sorted_coefficients, fitted_normal_pdf):
            file.write(f'{degree},{coeff},{pdf_value}\n')

# Parameters
start_degree = 10
end_degree = 20
step = 5

# Generate and write to CSV files
for m in range(start_degree, end_degree + 1, step):
    file_name = f'polynomial_degree_{m}.csv'
    fit_and_write_to_csv(m, file_name)
