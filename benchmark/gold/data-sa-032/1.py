import pandas as pd

prices_with_citi = pd.read_csv("crisis_portfolio.csv", index_col=0, parse_dates=True)

# Remove the Citibank column
prices_without_citi = prices_with_citi.drop(columns=['Citibank'])

import pdb; pdb.set_trace()

# Find the time series of returns with and without Citibank
ret_with_citi = prices_with_citi.pct_change().dot([0.25, 0.25, 0.25, 0.25])
ret_without_citi = prices_without_citi.pct_change().dot([0.25, 0.25, 0.25])

# Find the average 30-day rolling window volatility as the standard deviation
vol_with_citi = ret_with_citi.rolling(30).std().dropna().rename("With Citi")
vol_without_citi = ret_without_citi.rolling(30).std().dropna().rename("Without Citi")

# Combine two volatilities into one Pandas DataFrame
vol = pd.concat([vol_with_citi, vol_without_citi], axis=1)

vol.to_csv('result.csv')