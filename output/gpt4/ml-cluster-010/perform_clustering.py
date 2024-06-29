import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the dataset
df = pd.read_csv('/workspace/covtype.csv')

# Drop the 'Cover_Type' column as it's not needed for clustering
df.drop(columns=['Cover_Type'], inplace=True)

# Standardize the features
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

# Perform KMeans clustering with 6 clusters
kmeans = KMeans(n_clusters=6, random_state=42)
df['Cluster'] = kmeans.fit_predict(df_scaled)

# Rename the columns as specified
df.columns = ['Feature_' + str(i) if 'Feature_' not in col else col for i, col in enumerate(df.columns[:-1], 1)] + ['Cluster']

# Save the clustering results to a CSV file
df.to_csv('/workspace/cluster.csv', index=False)
