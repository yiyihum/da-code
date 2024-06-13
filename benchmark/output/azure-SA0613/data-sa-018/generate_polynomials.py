import sympy as sp
import numpy as np
from scipy.stats import norm
import csv

# Function to generate the polynomial and its coefficients
def generate_polynomial(m):
    t = sp.symbols('t')
    polynomial = 1
    for i in range(1, m + 1):
        polynomial *= (1 + t**(i**2 + 1))
    return sp.expand(polynomial)

# Function to fit a normal distribution and write to CSV
def fit_normal_and_write_csv(m, file_name):
    # Generate polynomial and coefficients
    polynomial = generate_polynomial(m)
    coefficients = polynomial.as_coefficients_dict()
    
    # Extract degrees and coefficients
    degrees = sorted(coefficients.keys(), key=lambda x: sp.degree(x))
    coeffs = [int(coefficients[term]) for term in degrees]  # Convert to integers
    
    # Fit a normal distribution to the coefficients
    mu, std = norm.fit(coeffs)
    fitted_normal_pdf = norm.pdf(coeffs, mu, std)
    
    # Write to CSV
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Degree', 'Coefficient', 'Fitted_Normal_PDF'])
        for degree, coeff, pdf_val in zip(degrees, coeffs, fitted_normal_pdf):
            writer.writerow([sp.degree(degree), coeff, pdf_val])

# Generate CSV files for the specified degrees
for degree in range(10, 21, 5):
    file_name = f'polynomial_degree_{degree}.csv'
    fit_normal_and_write_csv(degree, file_name)

print("CSV files generated successfully.")
