import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load the dataset
df = pd.read_csv('/workspace/covtype.csv')

# Standardize the features
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

# Perform K-Means clustering with a chosen number of clusters
kmeans = KMeans(n_clusters=7, random_state=42)
df['Cluster'] = kmeans.fit_predict(df_scaled)

# Rename columns to match the required format
df.columns = ['Feature_' + str(i) if i < len(df.columns) - 1 else 'Cluster' for i in range(len(df.columns))]

# Save the clustering results to a CSV file
df.to_csv('/workspace/cluster.csv', index=False)
