import pandas as pd
import numpy as np
from scipy.stats import norm
from sympy import symbols, expand, collect, Poly
import csv

# Read the polynomial values from the CSV file
df = pd.read_csv('polynomial_values.csv')

# Define the range of degrees for the analysis
start_degree = 10
end_degree = 30
step = 5

# Define the symbol for polynomial expansion
t = symbols('t')

# Function to calculate the coefficients of the polynomial
def calculate_coefficients(m):
    polynomial = 1
    for i in range(1, m + 1):
        polynomial *= (1 + t**(2*i + 1))
    return [float(coeff) for coeff in Poly(polynomial, t).all_coeffs()]

# Function to fit a normal distribution and write to CSV
def fit_normal_and_write_csv(degree, coefficients):
    # Fit a normal distribution to the coefficients
    mu, std = norm.fit(coefficients)
    
    # Calculate the PDF of the normal distribution for each degree
    fitted_pdf = norm.pdf(coefficients, mu, std)
    
    # Prepare the data to be written to the CSV
    data_to_write = zip(range(degree, -1, -1), coefficients, fitted_pdf)
    
    # Write to the corresponding CSV file
    file_name = f'polynomial_degree_{degree}.csv'
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Degree', 'Coefficient', 'Fitted_Normal_PDF'])
        for row in data_to_write:
            writer.writerow(row)

# Perform the analysis for each degree step
for degree in range(start_degree, end_degree + 1, step):
    # Calculate the coefficients of the polynomial
    coeffs = calculate_coefficients(degree // 2)
    
    # Fit the normal distribution and write to CSV
    fit_normal_and_write_csv(degree, coeffs)

print("Analysis and CSV file generation completed.")
