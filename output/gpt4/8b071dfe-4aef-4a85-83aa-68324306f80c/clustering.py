import pandas as pd
from sklearn.cluster import KMeans

# Load the processed data
df = pd.read_csv('/workspace/processed_online_retail.csv')

# Use only the relevant features for clustering
features = df[['Quantity', 'Price', 'Country', 'Recency']]

# Choose a reasonable number of clusters (for example, 4)
n_clusters = 4
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
df['Cluster'] = kmeans.fit_predict(features)

# Prepare the dataframe with the specified column names
cluster_df = df[['Quantity', 'Price', 'Country', 'Recency', 'Cluster']].copy()
cluster_df.columns = ['Feature_1', 'Feature_2', 'Feature_3', 'Feature_4', 'Cluster']

# Save the clustering results to a CSV file
cluster_file_path = '/workspace/cluster.csv'
cluster_df.to_csv(cluster_file_path, index=False)
print(f"Clustering results saved to {cluster_file_path}")
