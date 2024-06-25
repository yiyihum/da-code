import pandas as pd
import matplotlib.pyplot as plt
import yaml

# Load the stock return data and set 'Date' as the index
returns = pd.read_csv('Big9Returns2017.csv', index_col='Date', parse_dates=True)

# Load the portfolio weights
portfolios = pd.read_csv('EfficientFrontierPortfoliosSlim.csv')

# Calculate equal weights for the equal-weight portfolio
equal_weights = [1/len(returns.columns)] * len(returns.columns)

# Identify the portfolio with the highest Sharpe ratio (assuming risk-free rate is 0)
# Sharpe ratio is calculated as Returns / Volatility
portfolios['SharpeRatio'] = portfolios['Returns'] / portfolios['Volatility']
max_sharpe_idx = portfolios['SharpeRatio'].idxmax()
max_sharpe_portfolio = portfolios.iloc[max_sharpe_idx]

# Extract the weights for the max sharpe ratio portfolio corresponding to the stock tickers
max_sharpe_weights = max_sharpe_portfolio.filter(regex=' weight').values

# Identify the portfolio with the global minimum volatility
min_vol_idx = portfolios['Volatility'].idxmin()
min_vol_portfolio = portfolios.iloc[min_vol_idx]

# Extract the weights for the min volatility portfolio corresponding to the stock tickers
min_vol_weights = min_vol_portfolio.filter(regex=' weight').values

# Calculate the cumulative returns for each portfolio strategy
cumulative_returns = (1 + returns).cumprod()
returns['Cumulative EW'] = cumulative_returns.dot(equal_weights)
returns['Cumulative MSR'] = cumulative_returns.dot(max_sharpe_weights)
returns['Cumulative GMV'] = cumulative_returns.dot(min_vol_weights)

# Load plot specifications from 'plot.yaml'
with open('plot.yaml', 'r') as file:
    plot_specs = yaml.safe_load(file)

# Create the line plot
plt.figure(figsize=plot_specs['figsize'])
plt.plot(returns.index, returns['Cumulative EW'], label=plot_specs['labels'][0])
plt.plot(returns.index, returns['Cumulative MSR'], label=plot_specs['labels'][2])
plt.plot(returns.index, returns['Cumulative GMV'], label=plot_specs['labels'][3])
plt.title(plot_specs['graph_title'])
plt.xlabel(plot_specs['x_label'])
plt.ylabel(plot_specs['y_label'])
plt.legend()
plt.savefig('result.jpg')
