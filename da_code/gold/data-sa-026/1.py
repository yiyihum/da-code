
import pandas as pd
import numpy as np
from scipy.stats import t

# 读取原始股票数据
data = pd.read_csv('portfolio.csv', parse_dates=['Date'], dayfirst=True)
data.set_index('Date', inplace=True)

# 定义权重向量（示例）
weights = np.array([0.25, 0.25, 0.25, 0.25])  # 假设每个股票的权重都是0.25

# 计算每日收益率
returns = data.pct_change().dropna()

# 计算投资组合的加权收益率
portfolio_returns = returns.dot(weights)

# 计算投资组合损失
crisis_losses = -portfolio_returns


# Fit the Student's t distribution to crisis losses
p = t.fit(crisis_losses)

# Compute the VaR_99 for the fitted distribution
VaR_99 = t.ppf(0.99, *p)

# Use the fitted parameters and VaR_99 to compute CVaR_99
tail_loss = t.expect( lambda y: y, args = (p[0],), loc = p[1], scale = p[2], lb = VaR_99 )
CVaR_99 = (1 / (1 - 0.99)) * tail_loss


print(CVaR_99)
