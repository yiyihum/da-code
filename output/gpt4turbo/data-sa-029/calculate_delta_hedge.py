import numpy as np
import scipy.stats as si
import csv

# Function to calculate the Black-Scholes value for a European put option
def black_scholes_put(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    put = K * np.exp(-r * T) * si.norm.cdf(-d2) - S * si.norm.cdf(-d1)
    return put

# Load the annualized volatility from the file
with open('annualized_volatility.csv', 'r') as file:
    sigma = float(file.read())

# Load the previously calculated put value and delta
with open('black_scholes_results.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        original_put_value = float(row['put_value'])
        put_delta = float(row['put_delta'])

# Given parameters
S_original = 70  # Original spot price
S_new = 69.5  # New spot price
K = 80  # Strike price
T = 0.5  # Time to maturity in years
r = 0.02  # Risk-free interest rate

# Calculate the new Black-Scholes put option value
new_put_value = black_scholes_put(S_new, K, T, r, sigma)

# Calculate the change in option value
change_in_option_value = new_put_value - original_put_value

# Compute the change in stock price
change_in_stock_price = S_new - S_original

# Adjust the change in option value by dividing it by the delta
adjusted_change_in_option_value = change_in_option_value / put_delta

# Sum the change in stock price and the adjusted change in option value
delta_hedge_result = change_in_stock_price + adjusted_change_in_option_value

# Save the delta hedge result to 'result.csv'
with open('result.csv', 'w', newline='') as csvfile:
    fieldnames = ['delta_hedge_result']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'delta_hedge_result': delta_hedge_result})

print(f"Delta hedge result: {delta_hedge_result}")
