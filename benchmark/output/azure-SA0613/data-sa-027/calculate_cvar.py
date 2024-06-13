import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Function to calculate the Conditional Value at Risk (CVaR)
def calculate_cvar(returns, weights, alpha=0.05):
    portfolio_returns = returns.dot(weights)
    portfolio_returns_sorted = np.sort(portfolio_returns)
    index = int(alpha * len(portfolio_returns_sorted))
    cvar = portfolio_returns_sorted[:index].mean()
    return cvar

# Function to optimize the portfolio weights
def optimize_portfolio(returns, alpha=0.05):
    num_assets = returns.shape[1]
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})  # Weights must sum to 1
    bounds = tuple((0, 1) for asset in range(num_assets))
    initial_weights = num_assets * [1. / num_assets, ]
    
    def min_cvar(weights):
        return calculate_cvar(returns, weights, alpha)
    
    result = minimize(min_cvar, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x

# Load the historical stock price data
data = pd.read_csv('/workspace/portfolio.csv', index_col='Date', parse_dates=True)

# Calculate daily returns
returns = data.pct_change().dropna()

# Optimize the portfolio
optimal_weights = optimize_portfolio(returns)

# Write the results to 'result.csv'
result_df = pd.DataFrame(optimal_weights, index=data.columns, columns=['Weight'])
result_df.to_csv('/workspace/result.csv')
print("Optimal weights calculated and saved to result.csv.")
