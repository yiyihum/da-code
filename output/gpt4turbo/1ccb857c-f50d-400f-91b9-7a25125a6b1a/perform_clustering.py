from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pandas as pd

# Load the dataset
data = pd.read_csv('Country-data.csv')

# Drop the 'country' column as it's not needed for clustering
data_clustering = data.drop('country', axis=1)

# Normalize the data
scaler = StandardScaler()
data_normalized = scaler.fit_transform(data_clustering)

# Assuming 3 clusters based on common practice
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(data_normalized)

# Add the cluster labels to the original dataframe
data['Cluster'] = clusters

# Prepare the output columns with the correct names
feature_columns = [f'Feature_{i+1}' for i in range(data_clustering.shape[1])]
data_output = data.rename(columns=dict(zip(data_clustering.columns, feature_columns)))

# Save the clustering results to a CSV file
output_columns = ['country'] + feature_columns + ['Cluster']
data_output = data_output[output_columns]
data_output.to_csv('/workspace/cluster.csv', index=False)
