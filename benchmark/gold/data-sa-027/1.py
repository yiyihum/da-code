import pandas as pd

names = {0: 'Citibank', 1: 'Morgan Stanley', 2: 'Goldman Sachs', 3: 'J.P. Morgan'}

# 读取原始股票数据
data = pd.read_csv('portfolio.csv', parse_dates=['Date'], dayfirst=True)
data.set_index('Date', inplace=True)

# 计算每日收益率
returns = data.pct_change()


from pypfopt.efficient_frontier import EfficientCVaR

# Create the efficient frontier for CVaR minimization
ec = EfficientCVaR(None, returns)

# Find the cVar-minimizing portfolio weights at the default 95% confidence level
optimal_weights = ec.min_cvar()

# Map the values in optimal_weights to the bank names
optimal_weights = {names[i] : optimal_weights[i] for i in optimal_weights}

# Display the optimal weights
print(optimal_weights)