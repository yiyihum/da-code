import sympy as sp
from scipy.stats import norm
import csv

# Define the symbol 't' globally
t = sp.symbols('t')

# Function to directly compute the coefficients for a given degree
def compute_coefficients_for_degree(m, degree):
    coefficients = [0] * (degree + 1)
    for i in range(m + 1):
        exp = (2 * i + 1) ** 3
        if exp > degree:
            break
        coefficients[exp] += 1
    return coefficients

# Function to fit normal distribution and write to CSV
def fit_normal_and_write_csv(degree, filename):
    # Compute coefficients directly for the given degree
    coefficients = compute_coefficients_for_degree(5, degree)  # m is fixed at 5 as per polynomial_values.csv

    # Filter out zero coefficients and their degrees
    non_zero_coeffs = [(i, c) for i, c in enumerate(coefficients) if c != 0]

    # Fit a normal distribution to the non-zero coefficients
    degrees, non_zero_coeffs_only = zip(*non_zero_coeffs)
    mu, std = norm.fit(non_zero_coeffs_only)
    normal_pdf_values = norm.pdf(degrees, mu, std) if std != 0 else [1.0] * len(non_zero_coeffs_only)

    # Write to CSV
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Degree', 'Coefficient', 'Fitted_Normal_PDF'])
        for degree, coeff, pdf_val in zip(degrees, non_zero_coeffs_only, normal_pdf_values):
            writer.writerow([degree, coeff, pdf_val])

# Fit normal distribution and write to CSV for degrees 10 and 15
fit_normal_and_write_csv(10, 'polynomial_degree_10.csv')
fit_normal_and_write_csv(15, 'polynomial_degree_15.csv')
