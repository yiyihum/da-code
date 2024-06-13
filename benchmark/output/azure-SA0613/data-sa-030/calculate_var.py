import pandas as pd

# Load the portfolio data
portfolio_df = pd.read_csv('/workspace/portfolio.csv', parse_dates=['Date'], dayfirst=True)

# Calculate daily returns for each stock
daily_returns = portfolio_df.set_index('Date').pct_change().dropna()

# Compute portfolio returns with equal weights
equal_weights = [1.0 / daily_returns.shape[1]] * daily_returns.shape[1]
portfolio_returns = daily_returns.dot(equal_weights)

# Determine the 95th percentile of the losses for each period
period_1_mask = (portfolio_returns.index.year >= 2005) & (portfolio_returns.index.year <= 2006)
period_2_mask = (portfolio_returns.index.year >= 2007) & (portfolio_returns.index.year <= 2009)

period_1_losses = portfolio_returns[period_1_mask]
period_2_losses = portfolio_returns[period_2_mask]

# Since we are interested in losses, we take the negative of the returns
period_1_var_95 = -period_1_losses.quantile(0.05)
period_2_var_95 = -period_2_losses.quantile(0.05)

# Output the results
print(f"95% VaR for 2005-2006: {period_1_var_95}")
print(f"95% VaR for 2007-2009: {period_2_var_95}")
