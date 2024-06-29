import pandas as pd
from sklearn.cluster import KMeans
from datetime import datetime

# Load the dataset with 'ISO-8859-1' encoding
file_path = 'Year 2009-2010.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Convert 'InvoiceDate' to datetime
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

# Calculate total spending per customer
data['TotalPrice'] = data['Quantity'] * data['Price']
customer_data = data.groupby('Customer ID').agg({
    'TotalPrice': 'sum',
    'Invoice': 'nunique',
    'InvoiceDate': 'max'
}).reset_index()

# Rename columns for clarity
customer_data.rename(columns={'Invoice': 'TotalOrders', 'InvoiceDate': 'LastPurchaseDate'}, inplace=True)

# Calculate recency in days from the last purchase date
most_recent_purchase = customer_data['LastPurchaseDate'].max()
customer_data['Recency'] = (most_recent_purchase - customer_data['LastPurchaseDate']).dt.days

# Select features for clustering
features = customer_data[['TotalPrice', 'TotalOrders', 'Recency']]

# Perform clustering
kmeans = KMeans(n_clusters=5, random_state=42)
customer_data['Cluster'] = kmeans.fit_predict(features)

# Save the cluster data to a CSV file
cluster_file_path = 'cluster.csv'
customer_data.to_csv(cluster_file_path, index=False, columns=['Customer ID', 'TotalPrice', 'TotalOrders', 'Recency', 'Cluster'])

print(f"Cluster data saved to {cluster_file_path}")
