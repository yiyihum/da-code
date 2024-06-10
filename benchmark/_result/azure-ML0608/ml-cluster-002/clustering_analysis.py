import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the dataset
df = pd.read_csv('/workspace/wine-clustering.csv')

# Standardize the features
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

# Apply KMeans clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(df_scaled)

# Prepare the DataFrame with processed features and cluster labels
processed_df = pd.DataFrame(df_scaled, columns=df.columns[:-1])
processed_df.columns = [f'Processed_Feature_{i}' for i in range(len(processed_df.columns))]
processed_df['Cluster'] = df['Cluster']

# Save the clustering results to a CSV file
processed_df.to_csv('/workspace/cluster.csv', index=False)
