import pandas as pd
import numpy as np

# Load stock data and benchmark data
stock_data = pd.read_csv('stock_data.csv', index_col='Date', parse_dates=True)
benchmark_data = pd.read_csv('benchmark_data.csv', index_col='Date', parse_dates=True)

# Calculate daily returns for the stocks and the benchmark
stock_returns = stock_data.pct_change().dropna()
benchmark_returns = benchmark_data['S&P 500'].pct_change().dropna()

# Align the indices of the stock returns and the benchmark returns using an inner join
aligned_data = pd.merge(stock_returns, benchmark_returns, left_index=True, right_index=True, how='inner')

# Calculate the excess returns by subtracting the benchmark returns from the stock returns
excess_returns = aligned_data[stock_data.columns] - aligned_data['S&P 500'].values.reshape(-1, 1)

# Calculate the mean of excess returns and the standard deviation of the excess returns
mean_excess_return = excess_returns.mean()
std_excess_return = excess_returns.std()

# Annualization factor for the Sharpe ratio (sqrt of the number of trading days)
annualization_factor = np.sqrt(252)

# Calculate the annualized Sharpe ratio
sharpe_ratio = annualization_factor * mean_excess_return / std_excess_return

# Prepare the results in the required format and save to 'result.csv'
results = pd.DataFrame({
    'stock': ['Amazon', 'Facebook'],
    'sharpe_ratio': [sharpe_ratio['Amazon'], sharpe_ratio['Facebook']]
})
results.to_csv('result.csv', index=False)
