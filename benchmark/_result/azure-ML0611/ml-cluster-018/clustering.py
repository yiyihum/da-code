import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load the preprocessed customer-level dataset
customer_df = pd.read_csv('/workspace/customer_data.csv')

# Drop the CustomerID column as it's not needed for clustering
customer_df.drop('CustomerID', axis=1, inplace=True)

# Normalize the data
scaler = StandardScaler()
normalized_features = scaler.fit_transform(customer_df[['TotalSpend', 'TotalQuantity', 'Recency']])

# Apply K-Means clustering
kmeans = KMeans(n_clusters=5, random_state=42)
clusters = kmeans.fit_predict(normalized_features)

# Add the cluster labels to the dataframe
customer_df['Cluster'] = clusters

# Prepare the dataframe for saving: include the processed features and cluster labels
processed_df = pd.DataFrame(normalized_features, columns=['Processed_Feature_1', 'Processed_Feature_2', 'Processed_Feature_3'])
processed_df['Cluster'] = clusters

# Save the clustering results to a CSV file
processed_df.to_csv('/workspace/cluster.csv', index=False)

# Print the first few rows of the dataframe with cluster labels
print(processed_df.head())
