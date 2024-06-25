import pandas as pd
import numpy as np
from scipy.stats import norm

# Constants for Black-Scholes model (assumed values)
risk_free_rate = 0.01  # risk-free rate
time_to_expiration = 1  # time to expiration in years
strike_price = 130  # strike price

# Read historical stock data
df = pd.read_csv('IBM - HistoricalQuotes.csv')

# Calculate daily returns
df['return'] = df['close'].pct_change()

# Calculate the annualized volatility
annualized_volatility = df['return'].std() * np.sqrt(252)

# Black-Scholes model function
def black_scholes(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = (S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))
    return call_price

# Calculate option prices with original and double volatility
current_stock_price = df['close'].iloc[-1]  # most recent closing price
option_price_original_vol = black_scholes(current_stock_price, strike_price, time_to_expiration, risk_free_rate, annualized_volatility)
option_price_double_vol = black_scholes(current_stock_price, strike_price, time_to_expiration, risk_free_rate, 2 * annualized_volatility)

# Save the results to a CSV file
results = pd.DataFrame({
    'Annualized Volatility': [annualized_volatility],
    'Option Price (Original Vol)': [option_price_original_vol],
    'Option Price (Double Vol)': [option_price_double_vol]
})
results.to_csv('result.csv', index=False)
