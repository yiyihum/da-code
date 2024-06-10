from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/Facebook_Live.csv')

# Selecting the relevant features for clustering
features = df[['num_reactions', 'num_comments', 'num_shares', 'num_likes', 'num_loves', 'num_wows', 'num_hahas', 'num_sads', 'num_angrys']]

# Standardizing the features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Applying K-Means clustering
kmeans = KMeans(n_clusters=5, random_state=42)
df['Cluster'] = kmeans.fit_predict(features_scaled)

# Preparing the dataframe for output
output_df = pd.DataFrame(features_scaled, columns=['Processed_Feature_' + str(i) for i in range(features_scaled.shape[1])])
output_df['Cluster'] = df['Cluster']

# Saving the clustering results to a CSV file
output_df.to_csv('/workspace/cluster.csv', index=False)
