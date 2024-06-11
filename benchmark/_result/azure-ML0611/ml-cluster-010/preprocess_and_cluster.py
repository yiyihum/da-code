from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/covtype.csv')

# Store the number of unique values in 'Cover_Type' before dropping the column
n_clusters = df['Cover_Type'].nunique()

# Drop the 'Cover_Type' column as it is not needed for clustering
df = df.drop(columns=['Cover_Type'])

# Standardize the features
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

# Apply K-Means clustering
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(df_scaled)

# Create a new dataframe with processed features and cluster labels
clustered_df = pd.DataFrame(df_scaled, columns=[f'Processed_Feature_{i}' for i in range(df_scaled.shape[1])])
clustered_df['Cluster'] = clusters

# Save the clustering results to a CSV file
clustered_df.to_csv('/workspace/cluster.csv', index=False)
