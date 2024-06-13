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

    # Fit a normal distribution to the coefficients
    mu, std = norm.fit([c for c in coefficients if c != 0])  # Fit only to non-zero coefficients
    normal_pdf_values = norm.pdf([i for i, c in enumerate(coefficients) if c != 0], mu, std)

    # Write to CSV
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Degree', 'Coefficient', 'Fitted_Normal_PDF'])
        for i, (coeff, pdf_val) in enumerate(zip(coefficients, normal_pdf_values)):
            if coeff != 0:  # Only write non-zero coefficients
                writer.writerow([i, coeff, pdf_val])

# Fit normal distribution and write to CSV for degrees 10 and 15
fit_normal_and_write_csv(10, 'polynomial_degree_10.csv')
fit_normal_and_write_csv(15, 'polynomial_degree_15.csv')
