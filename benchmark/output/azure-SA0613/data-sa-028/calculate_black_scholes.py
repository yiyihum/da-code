import pandas as pd
import numpy as np
from scipy.stats import norm

# Black-Scholes formula
def black_scholes(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# Load the historical quotes data to get the most recent closing price
data = pd.read_csv('IBM - HistoricalQuotes.csv')
most_recent_close = data['close'].iloc[-1]

# Assumed parameters
K = most_recent_close  # strike price
T = 1.0  # time to expiration (1 year)
r = 0.02  # risk-free interest rate (2%)

# Calculated volatility from the previous step
sigma = 0.20823549582127499

# Calculate Black-Scholes option prices
option_price_vol = black_scholes(most_recent_close, K, T, r, sigma)
option_price_2vol = black_scholes(most_recent_close, K, T, r, 2 * sigma)

# Write the results to the result.csv file
result_df = pd.DataFrame({
    'volatility': [sigma, 2 * sigma],
    'option_price': [option_price_vol, option_price_2vol]
})
result_df.to_csv('result.csv', index=False)
