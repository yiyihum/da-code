import pandas as pd

# Load the historical stock data
data = pd.read_csv('/workspace/GE - Historical.csv')

# Display the first few rows of the dataframe
print(data.head())
