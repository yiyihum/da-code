import pandas as pd
from scipy.stats import t
import numpy as np

# Load the dataset
df = pd.read_csv('portfolio.csv', parse_dates=['Date'], dayfirst=True)

# Filter the data for the 2008-2009 period
start_date = '2008-01-01'
end_date = '2009-12-31'
mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
df = df.loc[mask]

# Calculate daily returns as percentage changes
returns = df.iloc[:, 1:].pct_change().dropna()

# Calculate portfolio losses
portfolio_losses = returns.sum(axis=1) * -1

# Fit a Student's t-distribution to the portfolio losses
params = t.fit(portfolio_losses)

# Calculate the 99% Value at Risk (VaR)
alpha = 0.01
VaR_99 = t.ppf(alpha, *params)

# Calculate the 99% Conditional Value at Risk (CVaR)
# CVaR should be negative, representing a loss
CVaR_99 = -t.expect(lambda x: -x, args=(params[0],), loc=params[1], scale=params[2], lb=VaR_99)

# Save the results to result.csv
results = pd.DataFrame({'VaR_99': [VaR_99], 'CVaR_99': [CVaR_99]})
results.to_csv('result.csv', index=False)
