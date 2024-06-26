import pandas as pd
import numpy as np
from scipy.stats import t
from datetime import datetime

# Load the portfolio data
df = pd.read_csv('/workspace/portfolio.csv', parse_dates=['Date'], dayfirst=True)

# Filter data for the period 2008-2009
start_date = datetime(2008, 1, 1)
end_date = datetime(2009, 12, 31)
mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
df = df.loc[mask]

# Calculate daily returns
returns = df.iloc[:, 1:].pct_change().dropna()

# Calculate portfolio returns by assuming equal weight for simplicity
portfolio_returns = returns.mean(axis=1)

# Fit a Student's t-distribution to the portfolio returns
params = t.fit(portfolio_returns)

# Calculate the 99% CVaR
confidence_level = 0.99
degrees_of_freedom, loc, scale = params
# Calculate the inverse cumulative distribution function (quantile function)
t_quantile = t.ppf(confidence_level, degrees_of_freedom, loc, scale)
# Calculate the expected shortfall (CVaR) as the mean of the distribution beyond the VaR
x = np.linspace(t.ppf(0.01, degrees_of_freedom), t_quantile, 100)
cvar = t.expect(lambda x: x, args=(degrees_of_freedom,), loc=loc, scale=scale, lb=t_quantile, conditional=True)

# Save the result
result = pd.DataFrame({'CVaR': [cvar]})
result.to_csv('/workspace/result.csv', index=False)
