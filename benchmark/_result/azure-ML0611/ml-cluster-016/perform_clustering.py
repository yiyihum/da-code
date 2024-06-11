import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from datetime import datetime

# Load the preprocessed customer data
customer_data = pd.read_csv('/workspace/customer_data.csv')

# Convert InvoiceDate_min and InvoiceDate_max to datetime
customer_data['InvoiceDate_min'] = pd.to_datetime(customer_data['InvoiceDate_min'])
customer_data['InvoiceDate_max'] = pd.to_datetime(customer_data['InvoiceDate_max'])

# We will use RFM features for clustering
# Recency: Number of days since the last purchase
# Frequency: Number of purchases (we'll use the count of unique InvoiceDate values)
# Monetary: Total amount spent (Quantity * Price)

# Calculate Recency in days
current_date = datetime.now()
customer_data['Recency'] = (current_date - customer_data['InvoiceDate_max']).dt.days

# Calculate Frequency
customer_data['Frequency'] = customer_data.groupby('Customer ID_')['InvoiceDate_min'].transform('nunique')

# Calculate Monetary
customer_data['Monetary'] = customer_data['Quantity_sum'] * customer_data['Price_mean']

# Select RFM features for clustering
rfm_features = customer_data[['Recency', 'Frequency', 'Monetary']]

# Normalize the features
scaler = StandardScaler()
rfm_normalized = scaler.fit_transform(rfm_features)

# Perform K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42)  # We choose 3 clusters for demonstration purposes
customer_data['Cluster'] = kmeans.fit_predict(rfm_normalized)

# Save the processed features and cluster labels to a CSV file
clustered_data = customer_data[['Customer ID_', 'Recency', 'Frequency', 'Monetary', 'Cluster']]
clustered_data.columns = ['Processed_Feature_0', 'Processed_Feature_1', 'Processed_Feature_2', 'Processed_Feature_3', 'Cluster']
clustered_data.to_csv('/workspace/cluster.csv', index=False)

print("Clustering completed and saved to cluster.csv")
