import pandas as pd

# Load the dataset
df = pd.read_csv('Big9Returns2017.csv')

# Define equal weights for the equal-weight portfolio
equal_weights = pd.Series([1/9] * 9, index=df.columns[1:])

# Calculate cumulative returns for the default portfolio
# Cumulative product of (1 + returns) for each stock, then take the product of these cumulative products for the overall return
df['DefaultPortfolio'] = (1 + df.iloc[:, 1:]).cumprod(axis=0).prod(axis=1) - 1

# Calculate cumulative returns for the equal-weight portfolio
# Multiply by equal weights, sum across stocks for each day, then calculate the cumulative sum
df['EqualWeightPortfolio'] = (df.iloc[:, 1:] * equal_weights).sum(axis=1).cumsum()

# Calculate cumulative returns for the market value-weighted portfolio
# Assuming market values are equal for simplicity, as no market value data is provided
# Multiply by market values (same as equal weights in this case), sum across stocks for each day, then calculate the cumulative sum
df['MarketValueWeightedPortfolio'] = (df.iloc[:, 1:] * equal_weights).sum(axis=1).cumsum()

# Save the results to a new CSV file
df.to_csv('result.csv', index=False)
