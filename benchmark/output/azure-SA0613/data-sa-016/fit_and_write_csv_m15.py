import numpy as np
from scipy.stats import norm

# Actual degrees and coefficients for m=15 from the previous output
degrees_m15 = [
    # ... (list all degrees from the previous output)
]
coefficients_m15 = [
    # ... (list all coefficients from the previous output)
]

# Fit the coefficients to a normal distribution
mu_m15, std_m15 = norm.fit(coefficients_m15)

# Calculate the fitted normal PDF values
fitted_normal_pdf_m15 = norm.pdf(degrees_m15, mu_m15, std_m15)

# Write to CSV for m=15
file_name_m15 = 'polynomial_degree_15.csv'
with open(file_name_m15, 'w') as file:
    file.write('Degree,Coefficient,Fitted_Normal_PDF\n')
    for degree, coeff, pdf_value in zip(degrees_m15, coefficients_m15, fitted_normal_pdf_m15):
        file.write(f'{degree},{coeff},{pdf_value}\n')
