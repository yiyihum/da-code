import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/online_retail_II.csv')

# Display the first few rows of the dataframe
print(df.head())

# Check for missing values in the relevant columns
print(df[['CustomerID', 'InvoiceDate', 'UnitPrice']].isnull().sum())
