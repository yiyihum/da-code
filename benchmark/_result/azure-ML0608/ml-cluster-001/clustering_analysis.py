import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the dataset
df = pd.read_csv('Mall_Customers.csv')

# Select the relevant columns for clustering
X = df[['Annual Income (k$)', 'Spending Score (1-100)']].values

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply K-Means clustering
kmeans = KMeans(n_clusters=5, random_state=42)
kmeans.fit(X_scaled)

# Create a DataFrame with the clustering results
clusters = kmeans.labels_
results = pd.DataFrame(X_scaled, columns=['Feature_1', 'Feature_2'])
results['Cluster'] = clusters

# Save the results to 'cluster.csv'
results.to_csv('cluster.csv', index=False)
