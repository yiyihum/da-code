import pandas as pd
from scipy.stats import t
import numpy as np

# Load the portfolio data with the correct date parsing
df = pd.read_csv('portfolio.csv', parse_dates=['Date'], dayfirst=True)

# Filter the data for the years 2008-2009
start_date = '2008-01-01'
end_date = '2009-12-31'
mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
df_filtered = df.loc[mask]

# Calculate daily returns
returns = df_filtered.set_index('Date').pct_change().dropna()

# Calculate the portfolio returns by assuming equal weight for each stock
portfolio_returns = returns.mean(axis=1)

# Calculate the degrees of freedom, location, and scale parameters for the t-distribution
params = t.fit(portfolio_returns)

# Calculate the VaR at 99% confidence level
confidence_level = 0.99
VaR_99 = t.ppf(1 - confidence_level, *params)

# Calculate the CVaR at 99% confidence level
cvar_data = portfolio_returns[portfolio_returns <= VaR_99]
CVaR_99 = cvar_data.mean()

# Save the result to a CSV file
result = pd.DataFrame({'CVaR_99': [CVaR_99]})
result.to_csv('result.csv', index=False)
