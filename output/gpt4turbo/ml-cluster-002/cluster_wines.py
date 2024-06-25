import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load the dataset
df = pd.read_csv('wine-clustering.csv')

# Standardize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df)

# Apply K-Means clustering
# The number of clusters is not specified in the task, so I will use a common choice of 3 clusters
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(scaled_features)

# Create a new DataFrame with the scaled features and cluster labels
clustered_df = pd.DataFrame(scaled_features, columns=[f'Feature_{i+1}' for i in range(scaled_features.shape[1])])
clustered_df['Cluster'] = clusters

# Save the results to a CSV file
clustered_df.to_csv('result.csv', index=False)
