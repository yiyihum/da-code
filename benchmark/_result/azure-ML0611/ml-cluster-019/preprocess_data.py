import pandas as pd
from datetime import datetime

# Load the combined data
df = pd.read_csv('/workspace/combined_data.csv')

# Remove cancellation transactions
df = df[~df['Invoice'].str.contains('C', na=False)]

# Remove transactions with missing 'Customer ID'
df = df.dropna(subset=['Customer ID'])

# Convert 'Customer ID' from float to int (to remove the decimal part)
df['Customer ID'] = df['Customer ID'].astype(int)

# Convert 'InvoiceDate' to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Calculate total price
df['TotalPrice'] = df['Quantity'] * df['Price']

# RFM feature engineering
# Recency: Days since last purchase
# Frequency: Number of transactions
# Monetary: Total amount spent

# Get the most recent purchase date in the dataset for recency calculation
latest_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

# Create the RFM DataFrame
rfm = df.groupby('Customer ID').agg({
    'InvoiceDate': lambda x: (latest_date - x.max()).days,
    'Invoice': 'count',
    'TotalPrice': 'sum'
}).rename(columns={'InvoiceDate': 'Recency', 'Invoice': 'Frequency', 'TotalPrice': 'Monetary'})

# Reset index to bring 'Customer ID' back as a column
rfm.reset_index(inplace=True)

# Save the RFM DataFrame to a new CSV for clustering
rfm.to_csv('/workspace/rfm_data.csv', index=False)

# Output the first few rows of the RFM DataFrame
print(rfm.head())
