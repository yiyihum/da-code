from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset
data = pd.read_csv('Country-data.csv')

# Drop the 'country' column as it's not needed for clustering
data_clustering = data.drop('country', axis=1)

# Normalize the data
scaler = StandardScaler()
data_normalized = scaler.fit_transform(data_clustering)

# Use the elbow method to find the optimal number of clusters
inertia = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(data_normalized)
    inertia.append(kmeans.inertia_)

# Save the elbow curve as an image file
plt.figure(figsize=(8, 4))
plt.plot(range(1, 11), inertia, marker='o')
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.savefig('/workspace/elbow_plot.png')
