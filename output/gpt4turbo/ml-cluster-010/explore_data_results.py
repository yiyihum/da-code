import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

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

# Save the results to a CSV file
results_df = pd.DataFrame({
    'Number_of_Clusters': K,
    'Inertia': inertia,
    'Silhouette_Score': silhouette_scores
})
results_df.to_csv('/workspace/clustering_results.csv', index=False)

# Print out the results
print(results_df)
