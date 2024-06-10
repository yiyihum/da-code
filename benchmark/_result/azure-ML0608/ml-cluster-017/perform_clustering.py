import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load the preprocessed dataset
df = pd.read_csv('/workspace/preprocessed_data.csv')

# Determine the optimal number of clusters using the elbow method
inertia = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=0).fit(df)
    inertia.append(kmeans.inertia_)

# Plot the elbow graph
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), inertia, marker='o')
plt.title('Elbow Method For Optimal k')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.show()

# Choose the number of clusters (k) and perform K-Means clustering
# Here we assume the elbow is at k=3 for demonstration purposes
k = 3
kmeans = KMeans(n_clusters=k, random_state=0).fit(df)

# Add the cluster labels to the dataframe
df['Cluster'] = kmeans.labels_

# Save the clustering results to a CSV file
output_file = '/workspace/cluster.csv'
df.to_csv(output_file, index=False)

print(f'Clustering results saved to {output_file}')
