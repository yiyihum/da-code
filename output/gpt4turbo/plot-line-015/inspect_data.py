import pandas as pd

# Load the stock return data
returns = pd.read_csv('Big9Returns2017.csv')

# Display the first few rows of the DataFrame to understand its structure
print(returns.head())
