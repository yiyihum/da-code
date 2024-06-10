import pandas as pd
from datetime import datetime

# Load the dataset
file_path = '/workspace/Online Retail.xlsx'
data = pd.read_excel(file_path)

# Remove transactions with missing 'CustomerID'
data = data.dropna(subset=['CustomerID'])

# Convert 'CustomerID' from float to int (to remove the decimal part)
data['CustomerID'] = data['CustomerID'].astype(int)

# Create a 'TotalPrice' column
data['TotalPrice'] = data['Quantity'] * data['UnitPrice']

# Aggregate data by 'CustomerID'
customer_data = data.groupby('CustomerID').agg({
    'TotalPrice': 'sum',
    'Quantity': 'sum',
    'InvoiceDate': lambda x: (datetime.now() - x.max()).days
}).rename(columns={'InvoiceDate': 'Recency'})

# Save the aggregated data to a CSV file
customer_data.to_csv('/workspace/preprocessed_customers.csv')

print('Preprocessed customer data saved to /workspace/preprocessed_customers.csv')
