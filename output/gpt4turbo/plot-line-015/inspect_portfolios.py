import pandas as pd

# Load the portfolio weights
portfolios = pd.read_csv('EfficientFrontierPortfoliosSlim.csv')

# Display the first few rows of the DataFrame to understand its structure
print(portfolios.head())
