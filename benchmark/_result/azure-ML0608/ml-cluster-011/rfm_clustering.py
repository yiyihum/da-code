import pandas as pd
from sklearn.cluster import KMeans
from datetime import datetime

# Load the dataset with the correct encoding
df = pd.read_csv('/workspace/OnlineRetail.csv', encoding='ISO-8859-1')

# Convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%d-%m-%Y %H:%M')

# Calculate Monetary value (Quantity * UnitPrice)
df['Monetary'] = df['Quantity'] * df['UnitPrice']

# Drop rows with missing CustomerID
df = df.dropna(subset=['CustomerID'])

# Calculate Recency, Frequency, Monetary for each customer
current_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (current_date - x.max()).days,
    'InvoiceNo': 'count',
    'Monetary': 'sum'
}).rename(columns={'InvoiceDate': 'Recency', 'InvoiceNo': 'Frequency'})

# Normalize the RFM values
rfm_normalized = (rfm - rfm.mean()) / rfm.std()

# Determine the optimal number of clusters using the elbow method
sse = {}
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=1)
    kmeans.fit(rfm_normalized)
    sse[k] = kmeans.inertia_

optimal_k = min(sse, key=sse.get)

# Apply KMeans clustering
kmeans = KMeans(n_clusters=optimal_k, random_state=1)
rfm['Cluster'] = kmeans.fit_predict(rfm_normalized)

# Prepare the output dataframe
output_df = rfm_normalized.copy()
output_df.columns = ['Processed_Feature_' + str(i) for i in range(1, len(output_df.columns) + 1)]
output_df['Cluster'] = rfm['Cluster']

# Save the clustering results to a CSV file
output_df.to_csv('/workspace/cluster.csv', index=False)
