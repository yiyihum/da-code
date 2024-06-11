import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the dataset
df = pd.read_csv('/workspace/Facebook_Live.csv')

# Select numerical columns for clustering
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
data = df[numerical_cols]

# Standardize the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Perform K-Means clustering
kmeans = KMeans(n_clusters=5, random_state=42)
clusters = kmeans.fit_predict(data_scaled)

# Prepare the dataframe with processed features and cluster labels
processed_data = pd.DataFrame(data_scaled, columns=[f'Processed_Feature_{i}' for i in range(data_scaled.shape[1])])
processed_data['Cluster'] = clusters

# Save the clustering results to a CSV file
processed_data.to_csv('/workspace/cluster.csv', index=False)
