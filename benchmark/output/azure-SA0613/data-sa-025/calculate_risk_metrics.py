import pandas as pd
import numpy as np

# Load the portfolio data
portfolio_df = pd.read_csv('portfolio.csv', parse_dates=['Date'], dayfirst=True)

# Calculate daily returns as percentage change
daily_returns = portfolio_df.iloc[:, 1:].pct_change().dropna()

# Calculate daily portfolio loss as the negative average of daily returns
portfolio_loss = -daily_returns.mean(axis=1)

# Calculate the mean and standard deviation of the portfolio losses
mean_loss = portfolio_loss.mean()
std_dev_loss = portfolio_loss.std()

# Calculate the 95% Value at Risk (VaR)
VaR_95 = np.percentile(portfolio_loss, 5)

# Calculate the Conditional Value at Risk (CVaR) for the worst 5% of cases
CVaR_95 = portfolio_loss[portfolio_loss <= VaR_95].mean()

# Write the results to the result.csv file
results = pd.DataFrame({
    'Mean': [mean_loss],
    'Standard Deviation': [std_dev_loss],
    '95% VaR': [VaR_95],
    '95% CVaR': [CVaR_95]
})
results.to_csv('result.csv', index=False)
