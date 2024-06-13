import pandas as pd
from scipy.integrate import quad
import numpy as np

# Define the probability density function
def probability_density_function(x):
    return (1 / np.sqrt(2 * np.pi)) * np.exp(-((x - 10) ** 2) / 2)

# Load the CSV file
df = pd.read_csv('probability_density_function_result.csv')

# Calculate the probability for each row
def calculate_probability(row):
    a, b = row['Number_A'], row['Number_B']
    result, _ = quad(probability_density_function, a, b)
    return round(result, 2)

# Apply the function to each row
df['Probability'] = df.apply(calculate_probability, axis=1)

# Save the results back to the CSV file
df.to_csv('probability_density_function_result.csv', index=False)
