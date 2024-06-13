

import pandas as pd
from black_scholes import black_scholes, bs_delta
import numpy as np


# Load the stock price data
data = pd.read_csv('IBM - HistoricalQuotes.csv', parse_dates=['date'], dayfirst=True)
data.set_index('date', inplace=True)

# Calculate daily returns for the 'close' prices
IBM_returns = data['close'].pct_change().dropna()


# Compute the annualized standard deviation of `IBM` returns
sigma = np.sqrt(252) * IBM_returns.std()

# Compute the Black-Scholes value at IBM spot price 70
value = black_scholes(S = 70, X = 80, T = 0.5, r = 0.02, 
                      sigma = sigma, option_type = "put")
# Find the delta of the option at IBM spot price 70
delta = bs_delta(S = 70, X = 80, T = 0.5, r = 0.02, 
                 sigma = sigma, option_type = "put")

# Find the option value change when the price of IBM falls to 69.5
value_change = black_scholes(S = 69.5, X = 80, T = 0.5, r = 0.02, 
                             sigma = sigma, option_type = "put") - value

print( (69.5 - 70) + (1/delta) * value_change )