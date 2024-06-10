import pandas as pd
import matplotlib.pyplot as plt

# Read the returns data
df_returns = pd.read_csv('Big9Returns2017.csv')
df_returns['Date'] = pd.to_datetime(df_returns['Date'])
df_returns.set_index('Date', inplace=True)

# Portfolio weights for the default portfolio
default_weights = {
    'AAPL': 0.12, 'MSFT': 0.15, 'XOM': 0.08, 'JNJ': 0.05,
    'JPM': 0.09, 'AMZN': 0.10, 'GE': 0.11, 'FB': 0.14, 'T': 0.16
}

# Market capitalizations for the market value-weighted portfolio
market_caps = {
    'AAPL': 601.51, 'MSFT': 469.25, 'XOM': 349.5, 'JNJ': 310.48,
    'JPM': 299.77, 'AMZN': 356.94, 'GE': 268.88, 'FB': 331.57, 'T': 246.09
}

# Calculate total market cap
total_market_cap = sum(market_caps.values())

# Calculate market cap weights
market_cap_weights = {ticker: cap / total_market_cap for ticker, cap in market_caps.items()}

# Calculate the cumulative returns for each portfolio strategy
cumulative_returns = {
    'default': (df_returns * pd.Series(default_weights)).sum(axis=1).cumprod(),
    'equal_weight': (df_returns * (1/9)).sum(axis=1).cumprod(),
    'market_weight': (df_returns * pd.Series(market_cap_weights)).sum(axis=1).cumprod()
}

# Create a DataFrame from the cumulative returns
df_cumulative_returns = pd.DataFrame(cumulative_returns)

# Plotting the cumulative returns
plt.figure(figsize=(10, 6))
for strategy in df_cumulative_returns.columns:
    plt.plot(df_cumulative_returns.index, df_cumulative_returns[strategy], label=strategy.replace('_', ' ').title())

plt.title('Cumulative Returns Over Time')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend()
plt.savefig('result.jpg')
plt.close()
