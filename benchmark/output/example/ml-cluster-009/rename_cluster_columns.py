import pandas as pd

# Load the cluster results
df = pd.read_csv('/workspace/cluster.csv')

# Rename the feature columns to "Feature_i"
feature_columns = df.columns[:-1]  # Exclude the 'Cluster' column
renamed_columns = {old_name: f'Feature_{i+1}' for i, old_name in enumerate(feature_columns)}
df.rename(columns=renamed_columns, inplace=True)

# Save the updated results to a CSV file
df.to_csv('/workspace/cluster.csv', index=False)
