from sympy import symbols, expand, Poly
import numpy as np
import scipy
import csv

# Function generating the new polynomial based on the given form
def generate_polynomial(n):
    t = symbols('t')
    polynomial = 1
    
    for i in range(1, n + 1):
        polynomial *= (1 + t**((2*i + 1)**2))
    
    expanded_polynomial = expand(polynomial)
    coefficients = Poly(expanded_polynomial, t).all_coeffs()
    
    return coefficients

# Function to get the distribution matched with normal pdf
def get_distribution(polynom_degrees, polynom_coeffs):
    mean = np.sum(polynom_degrees * polynom_coeffs) / np.sum(polynom_coeffs)
    variance = np.sum((polynom_degrees - mean)**2 * polynom_coeffs) / np.sum(polynom_coeffs)
    std = np.sqrt(variance)
    
    # Fitted distribution
    pdf = scipy.stats.norm.pdf(polynom_degrees, loc=mean, scale=std)
    
    return pdf

# Function to save coefficients and distribution to CSV
def save_coeffs_and_normal_pdf_to_csv(degree, filename):
    # Get coefficients
    coefficients = generate_polynomial(degree)
    int_coefficients = [int(coef) for coef in coefficients]
    
    # Get degrees
    degrees = [index for index, _ in enumerate(int_coefficients)]
    
    # Fit with normal distribution
    pdf_fitted = get_distribution(np.array(degrees), np.array(int_coefficients))
    
    # Save to CSV
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Degree', 'Coefficient', 'Fitted_Normal_PDF']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for deg, coef, pdf in zip(degrees, int_coefficients, pdf_fitted):
            writer.writerow({'Degree': deg, 'Coefficient': coef, 'Fitted_Normal_PDF': pdf})
    
    print(f'Saved coefficients and fitted normal distribution for degree {degree} to {filename}')

# Function to save results for a range of degrees
def save_degree_variation_to_csv(start_degree, end_degree, step):
    for degree in range(start_degree, end_degree + 1, step):
        filename = f'polynomial_degree_{degree}.csv'
        save_coeffs_and_normal_pdf_to_csv(degree, filename)

# Parameters for different degrees checking
np.seterr(divide='ignore')

start_degree = 10
end_degree = 20
step = 5
save_degree_variation_to_csv(start_degree, end_degree, step)
