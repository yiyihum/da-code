import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score

# Load the dataset with the correct delimiter
data = pd.read_csv('marketing_campaign.csv', delimiter='\t')

# Separate features and ID
X = data.drop('ID', axis=1)

# Preprocessing
# Identify categorical and numerical columns
categorical_cols = X.select_dtypes(include=['object']).columns
numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns

# Create transformers for numerical and categorical data
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine transformers into a preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Preprocess the data
X_preprocessed = preprocessor.fit_transform(X)

# Determine the optimal number of clusters using the Elbow method
inertia = []
silhouette_scores = []
K = range(2, 11)
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_preprocessed)
    inertia.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_preprocessed, kmeans.labels_))

# Based on the Elbow method and Silhouette scores, choose a reasonable number of clusters
# This is a placeholder for the chosen number of clusters
chosen_k = 5

# Apply KMeans clustering with the chosen number of clusters
kmeans = KMeans(n_clusters=chosen_k, random_state=42)
clusters = kmeans.fit_predict(X_preprocessed)

# Save the clustering results
data['Cluster'] = clusters
data.to_csv('cluster.csv', index=False, columns=[*X.columns, 'Cluster'])
