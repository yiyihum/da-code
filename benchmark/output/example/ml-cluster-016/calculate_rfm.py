import pandas as pd
from datetime import datetime

# Load the dataset
df = pd.read_csv('/workspace/online_retail_II.csv')

# Drop rows with missing 'Customer ID'
df = df.dropna(subset=['Customer ID'])

# Convert 'InvoiceDate' to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Calculate Recency as days since last purchase
most_recent_date = df['InvoiceDate'].max()
df['Recency'] = (most_recent_date - df['InvoiceDate']).dt.days

# Calculate Frequency as the number of unique invoices per customer
frequency_df = df.groupby('Customer ID')['Invoice'].nunique().reset_index()
frequency_df.columns = ['Customer ID', 'Frequency']

# Calculate Monetary as the total spent per customer
df['TotalPrice'] = df['Quantity'] * df['Price']
monetary_df = df.groupby('Customer ID')['TotalPrice'].sum().reset_index()
monetary_df.columns = ['Customer ID', 'Monetary']

# Merge the RFM metrics into a single dataframe
rfm_df = frequency_df.merge(monetary_df, on='Customer ID')
rfm_df['Recency'] = df.groupby('Customer ID')['Recency'].min().reset_index()['Recency']

# Save the RFM dataframe to a CSV file for further analysis
rfm_df.to_csv('/workspace/rfm_data.csv', index=False)

# Output the first few rows of the RFM dataframe
print(rfm_df.head())
