import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime

# Load the dataset
df = pd.read_csv('/workspace/online_retail_II.csv')

# Convert InvoiceDate to datetime and Customer ID to string
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Customer ID'] = df['Customer ID'].astype(str)

# Remove records with missing Customer IDs
df = df[~df['Customer ID'].isnull()]

# Remove cancelled transactions
df = df[~df['Invoice'].str.contains('C', na=False)]

# Calculate total price
df['TotalPrice'] = df['Quantity'] * df['Price']

# Aggregate data by Customer ID
customer_df = df.groupby('Customer ID').agg({
    'TotalPrice': 'sum',
    'Invoice': 'nunique',
    'InvoiceDate': 'max'
}).reset_index()

# Rename columns
customer_df.columns = ['CustomerID', 'TotalSpend', 'NumberOfTransactions', 'LastTransaction']

# Calculate recency in days
most_recent_date = customer_df['LastTransaction'].max()
customer_df['Recency'] = (most_recent_date - customer_df['LastTransaction']).dt.days

# Drop LastTransaction as it's no longer needed
customer_df = customer_df.drop('LastTransaction', axis=1)

# Extract features for clustering
features = customer_df[['TotalSpend', 'NumberOfTransactions', 'Recency']].values

# Scale the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Perform KMeans clustering
# The number of clusters is set to an arbitrary value for now, could be optimized with methods like the elbow method
kmeans = KMeans(n_clusters=5, random_state=42)
customer_df['Cluster'] = kmeans.fit_predict(scaled_features)

# Save the clustering results to a CSV file
customer_df.to_csv('/workspace/cluster.csv', index=False)

# Display the first few rows of the cluster DataFrame
print(customer_df.head())
