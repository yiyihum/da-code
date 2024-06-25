import pandas as pd
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# Load the dataset
df = pd.read_csv('03_Clustering_Marketing.csv')

# Select numerical features and drop any non-numerical ones
numerical_df = df.select_dtypes(include=['float64', 'int64'])

# Handle missing values by imputing with the mean
imputer = SimpleImputer(strategy='mean')
numerical_df_imputed = pd.DataFrame(imputer.fit_transform(numerical_df), columns=numerical_df.columns)

# Standardize the features
scaler = StandardScaler()
numerical_df_scaled = scaler.fit_transform(numerical_df_imputed)

# Perform clustering
kmeans = KMeans(n_clusters=5, random_state=42)
clusters = kmeans.fit_predict(numerical_df_scaled)

# Save the clustering results
result_df = pd.DataFrame(numerical_df_imputed, columns=numerical_df.columns)
result_df['Cluster'] = clusters
result_df.to_csv('cluster.csv', index=False)
