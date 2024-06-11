import pandas as pd
from datetime import datetime

# Load the data
df = pd.read_excel('/workspace/Online Retail.xlsx')

# Remove rows with missing CustomerID
df = df.dropna(subset=['CustomerID'])

# Remove cancellation transactions (those with negative Quantity)
df = df[df['Quantity'] > 0]

# Convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Create a TotalPrice column
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Aggregate data by CustomerID
customer_df = df.groupby('CustomerID').agg({
    'TotalPrice': 'sum',
    'Quantity': 'sum',
    'InvoiceDate': lambda x: (datetime.now() - x.max()).days
}).reset_index()

# Rename columns for clarity
customer_df.columns = ['CustomerID', 'TotalSpend', 'TotalQuantity', 'Recency']

# Print the first few rows of the aggregated customer-level dataset
print(customer_df.head())
