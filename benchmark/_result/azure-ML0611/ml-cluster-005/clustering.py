import pandas as pd
from sklearn.cluster import KMeans

# Load the dataset
df = pd.read_csv('/workspace/blob_dataset.csv')

# Select only the feature columns for clustering
X = df[['x', 'y']]

# Apply KMeans clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(X)

# Prepare the output dataframe with the required column names
output_df = X.copy()
output_df.columns = ['Processed_Feature_0', 'Processed_Feature_1']
output_df['Cluster'] = df['Cluster']

# Write the clustering results to a CSV file
output_df.to_csv('/workspace/cluster.csv', index=False)
