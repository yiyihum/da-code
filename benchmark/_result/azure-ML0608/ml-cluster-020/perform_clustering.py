import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load the dataset
df = pd.read_csv('IRIS.csv')

# Drop the 'species' column
df_features = df.drop(columns=['species'])

# Scale the features
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_features)

# Perform K-Means clustering with 3 clusters
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(df_scaled)

# Prepare the dataframe with processed features and cluster labels
processed_df = pd.DataFrame(df_scaled, columns=['Processed_Feature_0', 'Processed_Feature_1', 'Processed_Feature_2', 'Processed_Feature_3'])
processed_df['Cluster'] = df['Cluster']

# Save the clustering results to cluster.csv
processed_df.to_csv('cluster.csv', index=False)
