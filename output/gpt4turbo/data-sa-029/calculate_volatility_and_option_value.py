import pandas as pd
import numpy as np
from scipy.stats import norm

# Load the preprocessed data
data = pd.read_csv('preprocessed_ibm_data.csv', index_col='date')

# Calculate daily returns
data['returns'] = data['close'].pct_change()

# Compute annualized volatility (standard deviation of the daily returns)
daily_volatility = data['returns'].std()
annualized_volatility = daily_volatility * np.sqrt(252)  # Assuming 252 trading days in a year

# Black-Scholes model parameters for a European put option
S = 70  # Spot price
X = 80  # Strike price
T = 0.5  # Time to maturity in years
r = 0.02  # Risk-free interest rate
sigma = annualized_volatility  # Volatility

# Black-Scholes formula for put option price
d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)
put_option_price = X * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# Calculate the delta of the put option
delta_put = norm.cdf(d1) - 1

# Save the results to a new CSV file
results = pd.DataFrame({
    'annualized_volatility': [annualized_volatility],
    'put_option_price': [put_option_price],
    'delta_put': [delta_put]
})
results.to_csv('option_valuation.csv', index=False)
