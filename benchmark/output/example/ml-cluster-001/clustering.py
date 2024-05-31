import pandas as pd
from sklearn.cluster import KMeans

# Load the dataset
df = pd.read_csv('Mall_Customers.csv')

# Select the columns for clustering
X = df[['Annual Income (k$)', 'Spending Score (1-100)']]

# Perform KMeans clustering
kmeans = KMeans(n_clusters=5, random_state=0).fit(X)

# Add the clustering labels to the dataframe
df['Cluster'] = kmeans.labels_

# Write the clustering results into a new CSV file
df.to_csv('cluster.csv', index=False)