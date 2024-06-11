import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load the dataset
df = pd.read_csv('/workspace/wine-clustering.csv')

# Preprocess the data with standard scaling
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df)

# Perform K-Means clustering
# The number of clusters is not specified in the task, so I will assume a common choice of 3 clusters,
# as the original dataset was about three different cultivars of wine.
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(scaled_features)

# Create a new DataFrame with processed features and cluster labels
processed_df = pd.DataFrame(scaled_features, columns=[f'Processed_Feature_{i}' for i in range(1, len(df.columns) + 1)])
processed_df['Cluster'] = clusters

# Save the DataFrame to a CSV file
processed_df.to_csv('/workspace/cluster.csv', index=False)
