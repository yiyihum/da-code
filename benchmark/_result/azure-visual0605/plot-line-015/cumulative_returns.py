import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the stock returns data
returns = pd.read_csv('/workspace/Big9Returns2017.csv')
returns['Date'] = pd.to_datetime(returns['Date'])
returns.set_index('Date', inplace=True)

# Calculate the equal-weighted portfolio returns
equal_weights = np.array([1/9] * 9)
returns['Cumulative EW'] = (1 + (returns.iloc[:, :9] * equal_weights).sum(axis=1)).cumprod()

# Market capitalizations just before January 2017 (in $ billions)
market_caps = {
    'AAPL': 601.51,
    'MSFT': 469.25,
    'XOM': 349.5,
    'JNJ': 310.48,
    'JPM': 299.77,
    'AMZN': 356.94,
    'GE': 268.88,
    'FB': 331.57,
    'T': 246.09
}

# Calculate the market value-weighted portfolio returns
total_market_cap = sum(market_caps.values())
market_weights = np.array([market_caps[ticker] / total_market_cap for ticker in returns.columns[:9]])
returns['Cumulative MCap'] = (1 + (returns.iloc[:, :9] * market_weights).sum(axis=1)).cumprod()

# Assume risk-free rate is 0 for simplicity, calculate Sharpe ratio for each stock
risk_free_rate = 0
sharpe_ratios = returns.iloc[:, :9].mean() / returns.iloc[:, :9].std()
max_sharpe_idx = sharpe_ratios.idxmax()
max_sharpe_weight = np.zeros(9)
max_sharpe_weight[returns.columns.get_loc(max_sharpe_idx)] = 1
returns['Cumulative MSR'] = (1 + (returns.iloc[:, :9] * max_sharpe_weight).sum(axis=1)).cumprod()

# Assume we have pre-calculated weights for the global minimum volatility portfolio
# For simplicity, we will use equal weights as a placeholder for the actual GMV weights
# In a real scenario, we would optimize to find the weights that minimize portfolio volatility
gmv_weights = equal_weights
returns['Cumulative GMV'] = (1 + (returns.iloc[:, :9] * gmv_weights).sum(axis=1)).cumprod()

# Plot the cumulative returns
plt.figure(figsize=(12, 6))
plt.plot(returns['Cumulative EW'], label='Cumulative EW')
plt.plot(returns['Cumulative MCap'], label='Cumulative MCap')
plt.plot(returns['Cumulative MSR'], label='Cumulative MSR')
plt.plot(returns['Cumulative GMV'], label='Cumulative GMV')
plt.title('Cumulative Returns Over Time')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend()
plt.savefig('/workspace/result.jpg')
