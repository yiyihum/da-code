import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load the preprocessed customer data
customer_data_path = '/workspace/preprocessed_customers.csv'
customer_data = pd.read_csv(customer_data_path)

# Normalize the features
scaler = StandardScaler()
customer_data_scaled = scaler.fit_transform(customer_data[['TotalPrice', 'Quantity', 'Recency']])

# Predefined number of clusters for the purpose of this task
N = 5

# Apply K-means clustering
kmeans = KMeans(n_clusters=N, init='k-means++', max_iter=300, n_init=10, random_state=0)
clusters = kmeans.fit_predict(customer_data_scaled)

# Add the cluster labels to the customer data
customer_data['Cluster'] = clusters

# Prepare the dataframe with the required format
clustered_data = pd.DataFrame(customer_data_scaled, columns=['Processed_Feature_0', 'Processed_Feature_1', 'Processed_Feature_2'])
clustered_data['Cluster'] = customer_data['Cluster']

# Save the clustering results to a CSV file
output_file = '/workspace/cluster.csv'
clustered_data.to_csv(output_file, index=False)

print(f'Clustering completed with {N} clusters. Results saved to {output_file}.')
