import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score

# Load the dataset
df = pd.read_csv('/workspace/customer_segmentation.csv')

# Drop the ID column as it's not useful for clustering
df.drop('ID', axis=1, inplace=True)

# Convert Dt_Customer to datetime with the correct format and extract more meaningful features
df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], format='%d-%m-%Y')
df['Customer_Year'] = df['Dt_Customer'].dt.year
df['Customer_Month'] = df['Dt_Customer'].dt.month
df['Customer_Day'] = df['Dt_Customer'].dt.day
df.drop('Dt_Customer', axis=1, inplace=True)

# Select categorical and numerical columns
categorical_cols = df.select_dtypes(include=['object']).columns
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns

# Define the preprocessing steps for numerical and categorical data
numerical_preprocessor = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

categorical_preprocessor = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder())
])

# Combine preprocessing steps
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_preprocessor, numerical_cols),
        ('cat', categorical_preprocessor, categorical_cols)
    ])

# Define the clustering pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('cluster', KMeans(n_clusters=5, random_state=42))])

# Fit the pipeline to the data
pipeline.fit(df)

# Predict the clusters
clusters = pipeline.named_steps['cluster'].labels_

# Calculate silhouette score to evaluate the clustering
silhouette_avg = silhouette_score(pipeline.named_steps['preprocessor'].transform(df), clusters)
print(f'Silhouette Score: {silhouette_avg}')

# Add the cluster labels to the dataframe
df['Cluster'] = clusters

# Select only the numerical features and the cluster for the output file
output_df = df[numerical_cols.tolist() + ['Cluster']]

# Save the clustering results to a CSV file
output_df.to_csv('/workspace/cluster.csv', index=False)
