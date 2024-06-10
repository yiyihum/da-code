import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/covtype.csv')

# Display basic information about the dataset
print(df.info())

# Display the first few rows of the dataset to understand its structure
print(df.head())
