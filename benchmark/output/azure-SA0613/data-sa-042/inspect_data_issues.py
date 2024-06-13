import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/Books_df.csv')

# Inspect the first few entries in 'Price' and 'No. of People rated' columns
print("First few entries in 'Price':")
print(df['Price'].head())

print("\nFirst few entries in 'No. of People rated':")
print(df['No. of People rated'].head())
