import pandas as pd
from sklearn.cluster import KMeans
import numpy as np

# Load the dataset
df = pd.read_csv('/workspace/Mall_Customers.csv')

# Select the relevant columns for clustering
X = df[['Annual Income (k$)', 'Spending Score (1-100)']].values

# Determine the optimal number of clusters using the elbow method
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

# Find the elbow point which is the optimal number of clusters
optimal_clusters = np.argmax(np.diff(wcss)) + 1

# Perform KMeans clustering with the optimal number of clusters
kmeans = KMeans(n_clusters=optimal_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
clusters = kmeans.fit_predict(X)

# Create a DataFrame with the clustering results
cluster_df = pd.DataFrame({'Feature_1': X[:, 0], 'Feature_2': X[:, 1], 'Cluster': clusters})

# Write the clustering results to a CSV file
cluster_df.to_csv('/workspace/cluster.csv', index=False)
