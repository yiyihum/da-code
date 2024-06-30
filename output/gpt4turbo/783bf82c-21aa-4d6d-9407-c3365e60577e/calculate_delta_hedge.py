import pandas as pd
from scipy.stats import norm
import numpy as np

# Load the option valuation results
option_valuation = pd.read_csv('option_valuation.csv')
annualized_volatility = option_valuation['annualized_volatility'].iloc[0]
put_option_price = option_valuation['put_option_price'].iloc[0]
delta_put = option_valuation['delta_put'].iloc[0]

# Black-Scholes model parameters for a European put option with new stock price
S = 70  # Original spot price
S_new = 69.5  # New spot price
X = 80  # Strike price
T = 0.5  # Time to maturity in years
r = 0.02  # Risk-free interest rate
sigma = annualized_volatility  # Volatility

# Black-Scholes formula for put option price with new stock price
d1_new = (np.log(S_new / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2_new = d1_new - sigma * np.sqrt(T)
put_option_price_new = X * np.exp(-r * T) * norm.cdf(-d2_new) - S_new * norm.cdf(-d1_new)

# Calculate the change in option value
change_in_option_value = put_option_price_new - put_option_price

# Calculate the delta hedge result
change_in_stock_price = S_new - S
adjusted_change_in_option_value = change_in_option_value / delta_put
delta_hedge_result = change_in_stock_price + adjusted_change_in_option_value

# Compile the results in result.csv
results = pd.DataFrame({
    'change_in_stock_price': [change_in_stock_price],
    'adjusted_change_in_option_value': [adjusted_change_in_option_value],
    'delta_hedge_result': [delta_hedge_result]
})
results.to_csv('result.csv', index=False)
