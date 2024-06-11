# Create an array of market capitalizations (in billions)
market_capitalizations = np.array([601.51, 469.25, 349.5, 310.48, 299.77, 356.94, 268.88, 331.57, 246.09])

# Calculate the market cap weights
mcap_weights = market_capitalizations / sum(market_capitalizations)

# Calculate the market cap weighted portfolio returns
StockReturns['Portfolio_MCap'] = StockReturns.iloc[:, 0:9].mul(mcap_weights, axis=1).sum(axis=1)
# 计算累计收益率
StockReturns['Cumulative'] = (1 + StockReturns['Portfolio']).cumprod() - 1
StockReturns['Cumulative_EW'] = (1 + StockReturns['Portfolio_EW']).cumprod() - 1
StockReturns['Cumulative_MCap'] = (1 + StockReturns['Portfolio_MCap']).cumprod() - 1

# 将时间列（假设是索引）与三个累计收益率列合并到一个新的DataFrame中
CumulativeReturns_df = pd.DataFrame({
    'Date': StockReturns.index,  # 假设索引是日期
    'Cumulative': StockReturns['Cumulative'],
    'Cumulative_EW': StockReturns['Cumulative_EW'],
    'Cumulative_MCap': StockReturns['Cumulative_MCap']
}).set_index('Date')  # 你可以选择将日期设置为新DataFrame的索引

# 查看新创建的DataFrame
print(CumulativeReturns_df)  # 打印前几行来查看结果