from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Load the preprocessed customer data
customer_df = pd.read_csv('/workspace/preprocessed_customers.csv')

# Extract features for clustering
features = customer_df[['TotalSpend', 'NumberOfTransactions', 'Recency']].values

# Scale the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Perform KMeans clustering
# The number of clusters is set to an arbitrary value for now, could be optimized with methods like the elbow method
kmeans = KMeans(n_clusters=5, random_state=42)
customer_df['Cluster'] = kmeans.fit_predict(scaled_features)

# Save the clustering results to a CSV file
customer_df.to_csv('/workspace/cluster.csv', index=False)

# Display the first few rows of the cluster DataFrame
print(customer_df.head())
