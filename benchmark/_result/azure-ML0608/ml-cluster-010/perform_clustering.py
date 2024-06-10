import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np

# Load the dataset
df = pd.read_csv('/workspace/covtype.csv')

# Standardize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df)

# Apply PCA for dimensionality reduction
pca = PCA(n_components=0.95)  # Keep 95% of variance
principal_components = pca.fit_transform(scaled_features)
principal_df = pd.DataFrame(data=principal_components, columns=[f'Processed_Feature_{i}' for i in range(principal_components.shape[1])])

# Determine the optimal number of clusters using silhouette score
silhouette_scores = []
for n_clusters in range(2, 11):
    kmeans = KMeans(n_clusters=n_clusters)
    cluster_labels = kmeans.fit_predict(principal_df)
    silhouette_avg = silhouette_score(principal_df, cluster_labels)
    silhouette_scores.append((n_clusters, silhouette_avg))

# Choose the number of clusters with the highest silhouette score
optimal_n_clusters = max(silhouette_scores, key=lambda x: x[1])[0]

# Perform K-Means clustering with the optimal number of clusters
kmeans = KMeans(n_clusters=optimal_n_clusters)
principal_df['Cluster'] = kmeans.fit_predict(principal_df)

# Save the clustering results to a CSV file
principal_df.to_csv('/workspace/cluster.csv', index=False)
print(f'Clustering completed with {optimal_n_clusters} clusters.')
