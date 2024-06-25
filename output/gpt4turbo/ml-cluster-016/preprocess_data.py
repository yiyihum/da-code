import pandas as pd
from datetime import datetime
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load the dataset
df = pd.read_csv('/workspace/online_retail_II.csv')

# Drop rows with missing 'Customer ID'
df = df.dropna(subset=['Customer ID'])

# Convert 'InvoiceDate' to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Extract year, month, day, and possibly other features from 'InvoiceDate'
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month
df['Day'] = df['InvoiceDate'].dt.day
# Calculate recency in days from the last invoice date in the dataset
last_date = df['InvoiceDate'].max()
df['Recency'] = (last_date - df['InvoiceDate']).dt.days

# Drop columns that won't be used for clustering
df = df.drop(['Invoice', 'StockCode', 'Description', 'InvoiceDate'], axis=1)

# Normalize the 'Quantity' and 'Price' columns
scaler = StandardScaler()
df[['Quantity', 'Price']] = scaler.fit_transform(df[['Quantity', 'Price']])

# Encode the 'Country' column
encoder = LabelEncoder()
df['Country'] = encoder.fit_transform(df['Country'])

# Save the processed data to a new CSV file
processed_file_path = '/workspace/processed_online_retail.csv'
df.to_csv(processed_file_path, index=False)

print(f"Processed data saved to {processed_file_path}")
