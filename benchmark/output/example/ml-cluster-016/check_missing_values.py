import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/online_retail_II.csv')

# Check for missing values in the relevant columns
print(df[['Customer ID', 'InvoiceDate', 'Price']].isnull().sum())
