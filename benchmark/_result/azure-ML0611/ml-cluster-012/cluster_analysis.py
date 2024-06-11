import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score

# Load the dataset
df = pd.read_csv('/workspace/customer_segmentation.csv')

# Select features for clustering and drop the 'ID' column as it is not useful for clustering
features = df.drop(columns=['ID'])

# Define numerical and categorical features
numerical_features = features.select_dtypes(include=['int64', 'float64']).columns
categorical_features = features.select_dtypes(include=['object']).columns

# Preprocessing for numerical data: imputation of missing values and standardization
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

# Preprocessing for categorical data: imputation of missing values and one-hot encoding
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ], remainder='passthrough')

# Define the model
clusterer = KMeans(n_clusters=5, random_state=0)

# Create preprocessing and clustering pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('clusterer', clusterer)])

# Fit the pipeline to the data
pipeline.fit(features)

# Predict the cluster for each instance
clusters = pipeline.predict(features)

# Calculate silhouette score to evaluate the quality of clusters formed
silhouette_avg = silhouette_score(pipeline.named_steps['preprocessor'].transform(features), clusters)
print(f'Silhouette Score: {silhouette_avg}')

# Add the cluster labels to the dataframe
df['Cluster'] = clusters

# Get the processed features from the pipeline
processed_features = pipeline.named_steps['preprocessor'].transform(features)

# If the processed features are in a sparse matrix format, convert them to a dense array
if hasattr(processed_features, "toarray"):
    processed_features = processed_features.toarray()

# Create a DataFrame with the correct number of processed features
processed_df = pd.DataFrame(processed_features, columns=[f'Processed_Feature_{i}' for i in range(processed_features.shape[1])])
processed_df['Cluster'] = df['Cluster']

# Save the clustering results to a CSV file
processed_df.to_csv('/workspace/cluster.csv', index=False)
