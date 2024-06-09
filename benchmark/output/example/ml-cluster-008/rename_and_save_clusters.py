import pandas as pd

# Load the clustering results
cluster_data = pd.read_csv('/workspace/cluster.csv')

# Rename the columns to match the specified format "Feature_i"
feature_columns = ['Feature_' + str(i) for i in range(1, len(cluster_data.columns))]
cluster_data.columns = feature_columns + ['Cluster']

# Save the updated clustering results to a CSV file
cluster_data.to_csv('/workspace/cluster.csv', index=False)
