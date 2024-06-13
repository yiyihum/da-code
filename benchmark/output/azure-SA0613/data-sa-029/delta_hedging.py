import pandas as pd
import numpy as np
from scipy.stats import norm

# Load and preprocess the stock price data
data = pd.read_csv('IBM - HistoricalQuotes.csv', parse_dates=['date'])
data.set_index('date', inplace=True)

# Calculate daily returns
data['returns'] = data['close'].pct_change()

# Compute annualized volatility
volatility = data['returns'].std() * np.sqrt(252)

# Value the European put option using the Black-Scholes model
S = 70  # Spot price
X = 80  # Strike price
T = 0.5  # Time to maturity in years
r = 0.02  # Risk-free interest rate
sigma = volatility  # Volatility

# Black-Scholes formula for put option
d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)
put_option_value = X * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# Calculate the delta of the option
delta_put = -norm.cdf(-d1)

# Determine the change in option value for a new stock price
S_new = 69.5  # New stock price
d1_new = (np.log(S_new / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2_new = d1_new - sigma * np.sqrt(T)
put_option_value_new = X * np.exp(-r * T) * norm.cdf(-d2_new) - S_new * norm.cdf(-d1_new)
change_in_option_value = put_option_value_new - put_option_value

# Calculate and print the delta hedge result
change_in_stock_price = S_new - S
adjusted_change_in_option_value = change_in_option_value / delta_put
delta_hedge_result = change_in_stock_price + adjusted_change_in_option_value

# Print the result
print(delta_hedge_result)

# Save the result to result.csv
result = pd.DataFrame({'delta_hedge_result': [delta_hedge_result]})
result.to_csv('result.csv', index=False)
