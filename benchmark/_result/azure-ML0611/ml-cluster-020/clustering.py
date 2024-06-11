import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import numpy as np

# Load the dataset
df = pd.read_csv('/workspace/IRIS.csv')

# Selecting the features for clustering
features = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]

# Standardizing the features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Using the elbow method to find the optimal number of clusters
inertia = []
silhouette_scores = []
K_range = range(2, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(features_scaled)
    inertia.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(features_scaled, kmeans.labels_))

# Choosing the number of clusters with the highest silhouette score
optimal_k = K_range[np.argmax(silhouette_scores)]
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
kmeans.fit(features_scaled)

# Adding the cluster labels to the dataframe
df['Cluster'] = kmeans.labels_

# Preparing the dataframe with processed features and cluster labels
processed_df = pd.DataFrame(features_scaled, columns=['Processed_Feature_1', 'Processed_Feature_2', 'Processed_Feature_3', 'Processed_Feature_4'])
processed_df['Cluster'] = df['Cluster']

# Saving the clustering results to a CSV file
processed_df.to_csv('/workspace/cluster.csv', index=False)
