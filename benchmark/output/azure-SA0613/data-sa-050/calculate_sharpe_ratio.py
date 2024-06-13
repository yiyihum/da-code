import pandas as pd

# Load the dataset
df = pd.read_csv('faang_stocks.csv')

# Calculate daily returns
daily_returns = df.set_index('Date').pct_change()

# Calculate the average daily return of the portfolio
average_daily_returns = daily_returns.mean(axis=1)

# Calculate the annualized return of the portfolio (assuming 252 trading days in a year)
annualized_return = (1 + average_daily_returns).prod()**(252/len(df)) - 1

# Calculate the standard deviation of the portfolio's daily returns (portfolio risk)
portfolio_std_dev = average_daily_returns.std()

# Assuming a risk-free rate of 0% for simplicity
risk_free_rate = 0.0

# Calculate the Sharpe ratio
sharpe_ratio = (annualized_return - risk_free_rate) / portfolio_std_dev

# Write the results into the 'result.csv' file
results = pd.DataFrame({
    'Expected Annual Return': [annualized_return],
    'Sharpe Ratio': [sharpe_ratio]
})
results.to_csv('result.csv', index=False)
