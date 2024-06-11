import pandas as pd
from sklearn.cluster import KMeans

# Load the preprocessed data
df = pd.read_csv('/workspace/processed_bank_transactions.csv')

# Drop rows with missing values
df_clean = df.dropna()

# Perform K-Means clustering
# Using a fixed number of clusters for simplicity, as the Elbow method is not feasible within the current environment constraints
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(df_clean)

# Add the cluster labels to the dataframe
df_clean = df_clean.assign(Cluster=clusters)

# Prepare the final dataframe with processed features and cluster labels
# Assuming that the processed features are all the columns except 'Cluster'
processed_features = [col for col in df_clean.columns if col != 'Cluster']
final_df = df_clean[processed_features + ['Cluster']]

# Rename the columns to 'Processed_Feature_i'
for i, col in enumerate(processed_features):
    final_df.rename(columns={col: f'Processed_Feature_{i}'}, inplace=True)

# Save the clustering results to a new CSV file
cluster_file_path = '/workspace/cluster.csv'
final_df.to_csv(cluster_file_path, index=False)

cluster_file_path
