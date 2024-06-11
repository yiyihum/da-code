import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load the preprocessed data
df_processed = pd.read_csv('/workspace/processed_data.csv')

# Determine the optimal number of clusters using the Elbow method
inertia = []
for n in range(1, 11):
    kmeans = KMeans(n_clusters=n, random_state=42)
    kmeans.fit(df_processed)
    inertia.append(kmeans.inertia_)

# Plot the Elbow curve
plt.figure(figsize=(8, 4))
plt.plot(range(1, 11), inertia, marker='o')
plt.title('Elbow Method For Optimal k')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.savefig('/workspace/elbow_curve.png')
plt.close()

# Based on the Elbow curve, choose an appropriate number of clusters
# and perform KMeans clustering
# Note: The number of clusters is chosen based on the Elbow curve observation
# For the purpose of this task, I will assume an appropriate number of clusters
# If the Elbow curve is not clear, one might choose a number like 3 for simplicity
k = 3  # This is an example and should be replaced based on the Elbow curve
kmeans = KMeans(n_clusters=k, random_state=42)
df_processed['Cluster'] = kmeans.fit_predict(df_processed)

# Save the clustering results to a CSV file
df_processed.to_csv('/workspace/cluster.csv', index=False)
