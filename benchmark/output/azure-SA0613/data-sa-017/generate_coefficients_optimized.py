import sympy as sp
from scipy.stats import norm
import csv

# Define the symbol 't' globally
t = sp.symbols('t')

# Define the polynomial function
def generate_polynomial(m):
    polynomial = 1
    for i in range(1, m + 1):
        polynomial *= (1 + t ** ((2 * i + 1) ** 3))
    return polynomial

# Function to fit normal distribution and write to CSV
def fit_normal_and_write_csv(degree, filename):
    # Generate polynomial and get coefficients
    polynomial = generate_polynomial(degree)
    coeffs = polynomial.expand().as_ordered_terms()
    coefficients = [float(sp.Poly(term, t).coeffs()[0]) for term in coeffs if t in sp.Poly(term, t).gens]

    # Fit a normal distribution to the coefficients
    mu, std = norm.fit(coefficients)
    if std == 0:
        # If the standard deviation is zero, all coefficients are the same and the PDF is a delta function
        normal_pdf_values = [1.0] * len(coefficients)
    else:
        normal_pdf_values = norm.pdf(coefficients, mu, std)

    # Write to CSV
    with open(filename.format(degree), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Degree', 'Coefficient', 'Fitted_Normal_PDF'])
        for coeff, pdf_val in zip(coefficients, normal_pdf_values):
            writer.writerow([degree, coeff, pdf_val])

# Fit normal distribution and write to CSV for degrees 10 and 15
fit_normal_and_write_csv(10, 'polynomial_degree_10.csv')
fit_normal_and_write_csv(15, 'polynomial_degree_15.csv')
