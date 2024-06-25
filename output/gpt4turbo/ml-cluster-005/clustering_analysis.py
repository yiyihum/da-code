from sklearn.cluster import KMeans
import pandas as pd

# Load the dataset
df = pd.read_csv('blob_dataset.csv')

# Selecting only the feature columns for clustering
X = df[['x', 'y']]

# Applying K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
df['Cluster'] = kmeans.labels_

# Renaming columns to match the required format
df.rename(columns={'x': 'Feature_1', 'y': 'Feature_2'}, inplace=True)

# Selecting only the required columns to save
df_output = df[['Feature_1', 'Feature_2', 'Cluster']]

# Save the results to a CSV file
df_output.to_csv('cluster_blob.csv', index=False)
