import pandas as pd

# Load the data from the CSV file
data = pd.read_csv('/workspace/parts.csv')

# Check the first few rows of the dataframe to understand its structure
print(data.head())
