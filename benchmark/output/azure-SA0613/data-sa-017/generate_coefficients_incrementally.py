import sympy as sp
from scipy.stats import norm
import csv

# Define the symbol 't' globally
t = sp.symbols('t')

# Define the polynomial function
def generate_polynomial(m):
    terms = [(1 + t ** ((2 * i + 1) ** 3)) for i in range(1, m + 1)]
    return terms

# Function to calculate coefficients incrementally
def calculate_coefficients(terms):
    coeffs = [1]  # Start with the constant term
    for term in terms:
        term_coeffs = sp.Poly(term, t).all_coeffs()
        coeffs = sp.Poly(sp.expand(sum(sp.Mul(c, t**i) for i, c in enumerate(coeffs)) * term), t).all_coeffs()
    return [float(c) for c in coeffs]

# Function to fit normal distribution and write to CSV
def fit_normal_and_write_csv(degree, filename):
    # Generate polynomial terms and calculate coefficients incrementally
    terms = generate_polynomial(degree)
    coefficients = calculate_coefficients(terms)

    # Fit a normal distribution to the coefficients
    mu, std = norm.fit(coefficients)
    if std == 0:
        normal_pdf_values = [1.0] * len(coefficients)
    else:
        normal_pdf_values = norm.pdf(coefficients, mu, std)

    # Write to CSV
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Degree', 'Coefficient', 'Fitted_Normal_PDF'])
        for coeff, pdf_val in zip(coefficients, normal_pdf_values):
            writer.writerow([degree, coeff, pdf_val])

# Fit normal distribution and write to CSV for degrees 10 and 15
fit_normal_and_write_csv(10, 'polynomial_degree_10.csv')
fit_normal_and_write_csv(15, 'polynomial_degree_15.csv')
