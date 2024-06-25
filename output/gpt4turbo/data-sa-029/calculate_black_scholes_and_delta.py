import numpy as np
import scipy.stats as si

# Function to calculate the Black-Scholes value for a European put option
def black_scholes_put(S, K, T, r, sigma):
    # S: spot price
    # K: strike price
    # T: time to maturity
    # r: interest rate
    # sigma: volatility of underlying asset

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    put = K * np.exp(-r * T) * si.norm.cdf(-d2) - S * si.norm.cdf(-d1)
    return put

# Function to calculate the delta of a European put option
def delta_put(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    delta = -si.norm.cdf(-d1)
    return delta

# Load the annualized volatility from the file
with open('annualized_volatility.csv', 'r') as file:
    sigma = float(file.read())

# Given parameters
S = 70  # Spot price
K = 80  # Strike price
T = 0.5  # Time to maturity in years
r = 0.02  # Risk-free interest rate

# Calculate the Black-Scholes put option value
put_value = black_scholes_put(S, K, T, r, sigma)

# Calculate the delta of the put option
put_delta = delta_put(S, K, T, r, sigma)

# Save the results to a CSV file
results = {
    'put_value': put_value,
    'put_delta': put_delta
}

import csv
with open('black_scholes_results.csv', 'w', newline='') as csvfile:
    fieldnames = ['put_value', 'put_delta']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow(results)

print(f"Black-Scholes put option value: {put_value}")
print(f"Delta of the put option: {put_delta}")
