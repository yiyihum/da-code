import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans

# Load the dataset
df = pd.read_csv('/workspace/patient_dataset.csv')

# Separate features and categorical columns
numerical_features = df.select_dtypes(include=['int64', 'float64']).columns
categorical_features = df.select_dtypes(include=['object']).columns

# Preprocessing for numerical data: imputation
numerical_transformer = SimpleImputer(strategy='mean')

# Preprocessing for categorical data: imputation + one-hot encoding
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Preprocessing the data
X_preprocessed = preprocessor.fit_transform(df)

# Clustering
kmeans = KMeans(n_clusters=5, random_state=0)
df['Cluster'] = kmeans.fit_predict(X_preprocessed)

# Save the processed features and cluster labels to a new dataframe
processed_features = pd.DataFrame(X_preprocessed, columns=[f'Processed_Feature_{i}' for i in range(X_preprocessed.shape[1])])
clustered_data = pd.concat([processed_features, df['Cluster']], axis=1)

# Save the clustering results to a CSV file
clustered_data.to_csv('/workspace/cluster.csv', index=False)
