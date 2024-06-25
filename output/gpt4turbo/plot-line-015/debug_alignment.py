import pandas as pd

# Load the stock return data and set 'Date' as the index
returns = pd.read_csv('Big9Returns2017.csv', index_col='Date', parse_dates=True)

# Load the portfolio weights
portfolios = pd.read_csv('EfficientFrontierPortfoliosSlim.csv')

# Identify the portfolio with the highest Sharpe ratio (assuming risk-free rate is 0)
# Sharpe ratio is calculated as Returns / Volatility
portfolios['SharpeRatio'] = portfolios['Returns'] / portfolios['Volatility']
max_sharpe_idx = portfolios['SharpeRatio'].idxmax()
max_sharpe_weights = portfolios.iloc[max_sharpe_idx, :-3]  # Exclude the last 3 columns (Returns, Volatility, SharpeRatio)

# Identify the portfolio with the global minimum volatility
min_vol_idx = portfolios['Volatility'].idxmin()
min_vol_weights = portfolios.iloc[min_vol_idx, :-3]  # Exclude the last 3 columns (Returns, Volatility, SharpeRatio)

# Print the shapes of the returns DataFrame and the max_sharpe_weights Series
print("Shape of returns:", returns.shape)
print("Shape of max_sharpe_weights:", max_sharpe_weights.shape)
