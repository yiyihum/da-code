import sympy as sp
import numpy as np
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
def fit_normal_and_write_csv(start_degree, end_degree, step, filename):
    degrees = list(range(start_degree, end_degree + 1, step))
    for degree in degrees:
        # Generate polynomial and get coefficients
        polynomial = generate_polynomial(degree)
        coeffs = polynomial.expand().as_ordered_terms()
        coefficients = [float(sp.Poly(term, t).coeffs()[0]) for term in coeffs if t in sp.Poly(term, t).gens]

        # Fit a normal distribution to the coefficients
        mu, std = norm.fit(coefficients)
        normal_pdf_values = norm.pdf(coefficients, mu, std)

        # Write to CSV
        with open(filename.format(degree), mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Degree', 'Coefficient', 'Fitted_Normal_PDF'])
            for coeff, pdf_val in zip(coefficients, normal_pdf_values):
                writer.writerow([degree, coeff, pdf_val])

# Fit normal distribution and write to CSV for the specified degrees
fit_normal_and_write_csv(10, 15, 5, 'polynomial_degree_{}.csv')
