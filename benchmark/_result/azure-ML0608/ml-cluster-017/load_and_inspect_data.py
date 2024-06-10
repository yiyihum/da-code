import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/bank_transactions.csv')

# Display the first few rows of the dataframe
print(df.head())

# Display data types of the columns
print(df.dtypes)
