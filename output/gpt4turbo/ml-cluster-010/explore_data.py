import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/workspace/covtype.csv')

# Drop the 'Cover_Type' column as it's not needed for clustering
df.drop(columns=['Cover_Type'], inplace=True)

# Standardize the features
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

# Use the elbow method to determine the optimal number of clusters
inertia = []
silhouette_scores = []
K = range(2, 11)
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(df_scaled)
    inertia.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(df_scaled, kmeans.labels_))

# Plot the elbow graph
plt.figure(figsize=(14, 7))
plt.subplot(1, 2, 1)
plt.plot(K, inertia, 'bx-')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.title('The Elbow Method showing the optimal k')

# Plot the silhouette scores
plt.subplot(1, 2, 2)
plt.plot(K, silhouette_scores, 'bx-')
plt.xlabel('Number of clusters')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score for each k')

plt.savefig('/workspace/elbow_silhouette.png')
plt.close()
