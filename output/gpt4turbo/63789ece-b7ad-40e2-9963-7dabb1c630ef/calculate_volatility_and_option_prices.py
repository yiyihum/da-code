import pandas as pd
import numpy as np
from scipy.stats import norm

# Constants for Black-Scholes model
RISK_FREE_RATE = 0.01  # Assuming a risk-free rate of 1%
TRADING_DAYS = 252  # Number of trading days in a year

# Function to calculate the annualized volatility
def calculate_annualized_volatility(daily_returns):
    return np.std(daily_returns) * np.sqrt(TRADING_DAYS)

# Black-Scholes model function
def black_scholes(S, K, T, sigma, r=RISK_FREE_RATE, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        option_price = (S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))
    else:
        option_price = (K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1))
    return option_price

# Read the historical stock data
df = pd.read_csv('IBM - HistoricalQuotes.csv')

# Calculate daily returns
df['return'] = df['close'].pct_change()

# Drop the first row with NaN return
df = df.dropna()

# Calculate the annualized volatility
annual_volatility = calculate_annualized_volatility(df['return'])

# Assume some parameters for Black-Scholes model
S = df['close'].iloc[-1]  # Current stock price (most recent close price)
K = S  # Strike price (at-the-money option)
T = 1  # Time to expiration in years

# Calculate option prices
call_price_original_vol = black_scholes(S, K, T, annual_volatility)
call_price_double_vol = black_scholes(S, K, T, 2 * annual_volatility)

# Save the results to result.csv
result_df = pd.DataFrame({
    'Annual Volatility': [annual_volatility],
    'Call Price Original Vol': [call_price_original_vol],
    'Call Price Double Vol': [call_price_double_vol]
})
result_df.to_csv('result.csv', index=False)
