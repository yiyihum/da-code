import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Load the dataset
df = pd.read_csv('property.csv')

# Preprocess the data
# Replace boolean strings with integers and handle NaN values
df['has_elevator'] = df['has_elevator'].map({'true': 1, 'false': 0}).fillna(0).astype(int)
df['has_storage_area'] = df['has_storage_area'].map({'true': 1, 'false': 0}).fillna(0).astype(int)

# Handle missing values for all columns
imputer = SimpleImputer(strategy='mean')
df_imputed = imputer.fit_transform(df[['deposit', 'monthly_rent', 'room_qty', 'unit_area', 'has_elevator', 'building_floor_count', 'unit_floor', 'has_storage_area', 'property_age']])

# Standardize the features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(df_imputed)

# Perform clustering
kmeans = KMeans(n_clusters=4, random_state=0)
clusters = kmeans.fit_predict(features_scaled)

# Prepare the output dataframe
output_df = pd.DataFrame(features_scaled, columns=[f'Processed_Feature_{i}' for i in range(features_scaled.shape[1])])
output_df['Cluster'] = clusters

# Save the clustering results to a CSV file
output_df.to_csv('cluster.csv', index=False)
