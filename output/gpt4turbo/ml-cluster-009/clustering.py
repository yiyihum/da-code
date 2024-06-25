import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Load the dataset
df = pd.read_csv('world-data-2023.csv')

# Select numerical features for clustering
numerical_features = df.select_dtypes(include=['float64', 'int64'])

# Handle missing values by imputing with the mean
imputer = SimpleImputer(strategy='mean')
imputed_features = imputer.fit_transform(numerical_features)

# Standardize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(imputed_features)

# Perform KMeans clustering with 3 clusters
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(scaled_features)

# Prepare the dataframe with the original features and the cluster labels
clustered_data = pd.DataFrame(scaled_features, columns=numerical_features.columns)
clustered_data['Cluster'] = clusters

# Rename columns to "Feature_i"
clustered_data.columns = [f'Feature_{i}' if i < len(clustered_data.columns) - 1 else 'Cluster' for i in range(len(clustered_data.columns))]

# Save the results to a CSV file
clustered_data.to_csv('cluster.csv', index=False)
