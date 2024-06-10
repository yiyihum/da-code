import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load the scaled data
scaled_data = pd.read_csv('/workspace/scaled_data.csv')

# Determine the optimal number of clusters using the elbow method
wcss = []  # Within-cluster sum of squares
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(scaled_data)
    wcss.append(kmeans.inertia_)

# Plot the elbow graph
plt.figure(figsize=(10, 5))
plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
plt.title('Elbow Method to Determine Optimal Number of Clusters')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.savefig('/workspace/elbow_method.png')
plt.close()

# Choose the number of clusters as the point where the WCSS starts to level off
# This is usually the point with the maximum curvature (the elbow point)
optimal_clusters = 3  # This is an example, and the actual number should be determined from the plot

# Perform K-means clustering with the optimal number of clusters
kmeans = KMeans(n_clusters=optimal_clusters, init='k-means++', random_state=42)
clusters = kmeans.fit_predict(scaled_data)

# Add the cluster labels to the scaled data
clustered_data = scaled_data.copy()
clustered_data['Cluster'] = clusters

# Save the clustering results to a CSV file
clustered_data.to_csv('/workspace/cluster.csv', index=False)

print("Clustering complete and saved to cluster.csv.")
