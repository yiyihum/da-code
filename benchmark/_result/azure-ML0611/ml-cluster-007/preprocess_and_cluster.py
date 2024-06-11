import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer

# Load the dataset
df = pd.read_csv('/workspace/03_Clustering_Marketing.csv')

# Convert 'age' to numeric, coercing errors to NaN
df['age'] = pd.to_numeric(df['age'], errors='coerce')

# Handle missing values for 'age' by imputing with the median
imputer = SimpleImputer(strategy='median')
df['age'] = imputer.fit_transform(df[['age']])

# Encode 'gender' as a categorical variable
df['gender'] = df['gender'].fillna('Unknown')  # Handle missing values for gender
encoder = LabelEncoder()
df['gender'] = encoder.fit_transform(df['gender'])

# Normalize the data
scaler = StandardScaler()
feature_cols = [col for col in df.columns if col not in ['gradyear', 'gender', 'age', 'NumberOffriends']]
df[feature_cols] = scaler.fit_transform(df[feature_cols])

# Apply KMeans clustering
kmeans = KMeans(n_clusters=5, random_state=42)
df['Cluster'] = kmeans.fit_predict(df[feature_cols])

# Prepare the dataframe for output
output_df = df[feature_cols + ['Cluster']]
output_df.columns = [f'Processed_Feature_{i}' for i in range(len(feature_cols))] + ['Cluster']

# Save the clustering results to 'cluster.csv'
output_df.to_csv('/workspace/cluster.csv', index=False)
