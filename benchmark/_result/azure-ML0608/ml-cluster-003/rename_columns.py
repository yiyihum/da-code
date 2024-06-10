import pandas as pd

# Load the clustering results
cluster_df = pd.read_csv('/workspace/cluster.csv')

# Rename the columns to match the specified format
renamed_columns = [f'Processed_Feature_{i}' if not col.endswith('Cluster') else col for i, col in enumerate(cluster_df.columns)]
cluster_df.columns = renamed_columns

# Save the updated DataFrame to a CSV file
cluster_df.to_csv('/workspace/cluster.csv', index=False)
