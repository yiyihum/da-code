import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the RFM data
rfm = pd.read_csv('/workspace/rfm_data.csv')

# Normalize the RFM data
scaler = StandardScaler()
rfm_normalized = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])

# Perform K-Means clustering
kmeans = KMeans(n_clusters=5, init='k-means++', max_iter=300, n_init=10, random_state=0)
clusters = kmeans.fit_predict(rfm_normalized)

# Create a DataFrame with the cluster results
clustered_data = rfm.copy()
clustered_data['Cluster'] = clusters

# Rename the columns as specified in the task
clustered_data.rename(columns={
    'Recency': 'Processed_Feature_0',
    'Frequency': 'Processed_Feature_1',
    'Monetary': 'Processed_Feature_2'
}, inplace=True)

# Save the DataFrame to a CSV file
clustered_data.to_csv('/workspace/cluster.csv', index=False)

# Output the first few rows of the clustered DataFrame
print(clustered_data.head())
