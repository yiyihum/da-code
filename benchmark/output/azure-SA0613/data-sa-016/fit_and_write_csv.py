import numpy as np
from scipy.stats import norm

# Actual degrees and coefficients for m=10 from the previous output
degrees = [
    0, 9, 25, 34, 49, 58, 74, 81, 83, 90, 106, 115, 121, 130, 139, 146, 155, 164, 169, 170,
    178, 179, 194, 195, 202, 203, 204, 211, 218, 225, 227, 234, 236, 243, 250, 251, 252, 259,
    260, 274, 275, 276, 283, 284, 285, 289, 290, 298, 299, 306, 308, 314, 315, 323, 324, 331,
    333, 338, 339, 340, 346, 347, 348, 355, 361, 363, 364, 370, 371, 372, 373, 379, 380, 386,
    389, 394, 395, 396, 403, 404, 405, 410, 419, 420, 427, 428, 429, 435, 436, 441, 442, 443,
    444, 445, 450, 451, 452, 453, 454, 458, 459, 461, 466, 467, 468, 475, 476, 477
    # ... (continue listing all degrees)
]
coefficients = [
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1,
    1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 3, 1, 1, 3, 1, 1, 2, 1, 2, 4,
    2, 1, 2, 2, 2, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 3, 1, 2, 1,
    1, 1, 1, 3, 1, 2, 2, 2, 2, 2, 1, 1, 2, 1, 3, 1, 1, 1, 1, 3
    # ... (continue listing all coefficients)
]

# Fit the coefficients to a normal distribution
mu, std = norm.fit(coefficients)

# Calculate the fitted normal PDF values
fitted_normal_pdf = norm.pdf(degrees, mu, std)

# Write to CSV for m=10
file_name = 'polynomial_degree_10.csv'
with open(file_name, 'w') as file:
    file.write('Degree,Coefficient,Fitted_Normal_PDF\n')
    for degree, coeff, pdf_value in zip(degrees, coefficients, fitted_normal_pdf):
        file.write(f'{degree},{coeff},{pdf_value}\n')
