import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Load the dataset
df = pd.read_csv('/workspace/customer_segmentation.csv')

# Drop the 'ID' column as it is not relevant for clustering
df.drop('ID', axis=1, inplace=True)

# Handle missing values in 'Income' by imputing with the median
df['Income'] = df['Income'].fillna(df['Income'].median())

# Convert 'Dt_Customer' to datetime and extract potentially useful features
df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], format='%d-%m-%Y')
df['Customer_Year'] = df['Dt_Customer'].dt.year
df['Customer_Month'] = df['Dt_Customer'].dt.month
df['Customer_Day'] = df['Dt_Customer'].dt.day

# Drop the original 'Dt_Customer' column
df.drop('Dt_Customer', axis=1, inplace=True)

# Define the features to be included in the clustering
numerical_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_features = ['Education', 'Marital_Status']

# Create preprocessing pipelines for both numerical and categorical data
numerical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine preprocessing steps into a single ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_pipeline, numerical_features),
        ('cat', categorical_pipeline, categorical_features)
    ])

# Preprocess the data
X_processed = preprocessor.fit_transform(df)

# Determine the optimal number of clusters using silhouette score
silhouette_scores = []
for n_clusters in range(2, 11):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(X_processed)
    silhouette_avg = silhouette_score(X_processed, cluster_labels)
    silhouette_scores.append((n_clusters, silhouette_avg))

# Select the number of clusters with the highest silhouette score
optimal_n_clusters = max(silhouette_scores, key=lambda x: x[1])[0]

# Perform clustering with the optimal number of clusters
kmeans = KMeans(n_clusters=optimal_n_clusters, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_processed)

# Prepare the dataframe with processed features and cluster labels
processed_features = pd.DataFrame(X_processed, columns=[f'Processed_Feature_{i}' for i in range(X_processed.shape[1])])
clustered_df = pd.concat([processed_features, df['Cluster']], axis=1)

# Save the clustering results to a CSV file
clustered_df.to_csv('/workspace/cluster.csv', index=False)
