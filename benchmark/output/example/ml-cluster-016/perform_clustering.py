import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load the RFM data
rfm_df = pd.read_csv('/workspace/rfm_data.csv')

# Scale the RFM data
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_df[['Recency', 'Frequency', 'Monetary']])

# Determine the optimal number of clusters using the elbow method
sse = {}
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=1)
    kmeans.fit(rfm_scaled)
    sse[k] = kmeans.inertia_

# Plot SSE for each *k*
plt.figure()
plt.plot(list(sse.keys()), list(sse.values()))
plt.xlabel("Number of cluster")
plt.ylabel("SSE")
plt.show()

# Choose the optimal number of clusters (k) based on the elbow plot
# This is a manual step where we look at the plot and choose the k where the SSE starts to flatten out
# For the purpose of this task, let's assume the optimal number of clusters is 3
optimal_k = 3

# Perform K-means clustering with the optimal number of clusters
kmeans = KMeans(n_clusters=optimal_k, random_state=1)
rfm_df['Cluster'] = kmeans.fit_predict(rfm_scaled)

# Save the clustering results to 'cluster.csv'
cluster_columns = ['Feature_1', 'Feature_2', 'Feature_3', 'Cluster']
rfm_df.rename(columns={'Recency': 'Feature_1', 'Frequency': 'Feature_2', 'Monetary': 'Feature_3'}, inplace=True)
rfm_df[cluster_columns].to_csv('/workspace/cluster.csv', index=False)

# Output the first few rows of the clustering results
print(rfm_df[cluster_columns].head())
