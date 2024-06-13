import pandas as pd
import numpy as np

# Read stock price data
data = pd.read_csv('portfolio.csv', parse_dates=['Date'], dayfirst=True)
data.set_index('Date', inplace=True)

# Calculate daily returns for each stock
asset_returns = data.pct_change().dropna()

# Split data into two time periods
asset_returns_1 = asset_returns.loc['2005-01-03':'2006-12-29']
asset_returns_2 = asset_returns.loc['2007-01-03':'2009-12-31']

# Portfolio weights
weights = np.array([0.25, 0.25, 0.25, 0.25])

# Calculate portfolio returns for each sub-period
portfolio_returns_1 = asset_returns_1.dot(weights)
portfolio_returns_2 = asset_returns_2.dot(weights)

# Combine portfolio returns into one list
portfolio_returns = [portfolio_returns_1, portfolio_returns_2]

# Derive portfolio losses from portfolio returns
losses = [-x for x in portfolio_returns]

# Find the historical simulated VaR estimates
VaR_95 = [np.quantile(x, 0.95) for x in losses]

# Display the VaR estimates
print("VaR_95, 2005-2006: ", VaR_95[0], '; VaR_95, 2007-2009: ', VaR_95[1])
