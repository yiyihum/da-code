import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load the RFM data
rfm = pd.read_csv('/workspace/rfm_data.csv')

# Normalize the data
rfm_normalized = (rfm[['Recency', 'Frequency', 'Monetary']] - rfm[['Recency', 'Frequency', 'Monetary']].mean()) / rfm[['Recency', 'Frequency', 'Monetary']].std()

# Use the elbow method to find the optimal number of clusters
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(rfm_normalized)
    wcss.append(kmeans.inertia_)

# Plot the results to observe the elbow
plt.figure(figsize=(10, 8))
plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
plt.title('Elbow Method For Optimal k')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()
