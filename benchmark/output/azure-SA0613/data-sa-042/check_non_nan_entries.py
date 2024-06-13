import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/Books_df.csv')

# Convert 'Price' and 'No. of People rated' to numeric, coercing errors to NaN
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['No. of People rated'] = pd.to_numeric(df['No. of People rated'], errors='coerce')

# Drop rows with NaN values in these columns
df = df.dropna(subset=['Price', 'No. of People rated'])

# Check the number of non-NaN entries in both columns
non_nan_price = df['Price'].notna().sum()
non_nan_ratings = df['No. of People rated'].notna().sum()

# Print the number of non-NaN entries
print(f"Non-NaN entries in 'Price': {non_nan_price}")
print(f"Non-NaN entries in 'No. of People rated': {non_nan_ratings}")
