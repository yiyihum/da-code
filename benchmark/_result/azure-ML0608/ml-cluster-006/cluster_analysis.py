import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans

# Load the dataset
df = pd.read_csv('/workspace/patient_dataset.csv')

# Separate features and drop any non-feature columns if necessary
features = df.drop(columns=[])

# Define numerical and categorical features
numerical_features = features.select_dtypes(include=['int64', 'float64']).columns
categorical_features = features.select_dtypes(include=['object']).columns

# Create preprocessing pipelines for both numerical and categorical data
numerical_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),  # Impute missing values with mean
    ('scaler', StandardScaler())  # Scale data
])

categorical_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),  # Impute missing values with most frequent
    ('encoder', OneHotEncoder(handle_unknown='ignore'))  # Encode categorical data
])

# Combine preprocessing steps into a single ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_pipeline, numerical_features),
        ('cat', categorical_pipeline, categorical_features)
    ]
)

# Preprocess the data
X_processed = preprocessor.fit_transform(features)

# Perform clustering
kmeans = KMeans(n_clusters=3, random_state=42)  # Assuming 3 clusters for demonstration
clusters = kmeans.fit_predict(X_processed)

# Create a DataFrame with processed features and cluster labels
processed_features = pd.DataFrame(X_processed, columns=[f'Processed_Feature_{i}' for i in range(X_processed.shape[1])])
processed_features['Cluster'] = clusters

# Save the clustering results to a CSV file
processed_features.to_csv('/workspace/cluster.csv', index=False)
