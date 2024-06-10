import pandas as pd
from sklearn.cluster import KMeans

# Load the dataset
df = pd.read_csv('blob_dataset.csv')

# Select only the feature columns for clustering
X = df[['x', 'y']]

# Apply K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=0)  # Assuming 3 clusters from the 'label' column
df['Cluster'] = kmeans.fit_predict(X)

# Rename the columns as specified
df.rename(columns={'x': 'Processed_Feature_0', 'y': 'Processed_Feature_1'}, inplace=True)

# Save the clustering results to a CSV file
df[['Processed_Feature_0', 'Processed_Feature_1', 'Cluster']].to_csv('cluster.csv', index=False)
