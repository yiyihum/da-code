import pandas as pd
from black_scholes import black_scholes
import numpy as np


# Load the stock price data
data = pd.read_csv('IBM - HistoricalQuotes.csv', parse_dates=['date'], dayfirst=True)
data.set_index('date', inplace=True)

# Calculate daily returns for the 'close' prices
IBM_returns = data['close'].pct_change().dropna()



# Compute the volatility as the annualized standard deviation of IBM returns
sigma = np.sqrt(252) * IBM_returns.std()

# Compute the Black-Scholes option price for this volatility
value_s = black_scholes(S = 90, X = 80, T = 0.5, r = 0.02, 
                        sigma = sigma, option_type = "call")

# Compute the Black-Scholes option price for twice the volatility
value_2s = black_scholes(S = 90, X = 80, T = 0.5, r = 0.02, 
                         sigma = 2 * sigma, option_type = "call")

# Display and compare both values
print("Option value for sigma: ", value_s, "\n", 
      "Option value for 2 * sigma: ", value_2s)