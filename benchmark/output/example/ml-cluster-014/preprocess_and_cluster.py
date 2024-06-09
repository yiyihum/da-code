import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from kneed import KneeLocator

# Load the dataset with the correct delimiter
df = pd.read_csv('/workspace/marketing_campaign.csv', delimiter='\t')

# Drop the columns that are not useful for clustering
df.drop(['ID', 'Z_CostContact', 'Z_Revenue'], axis=1, inplace=True)

# Handle missing values for 'Income' by imputing with the median
df['Income'].fillna(df['Income'].median(), inplace=True)

# Select columns for one-hot encoding and standard scaling
categorical_features = ['Education', 'Marital_Status']
numerical_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

# Remove categorical features from the numerical features list
numerical_features = [feature for feature in numerical_features if feature not in categorical_features]

# Create transformers for the pipeline
categorical_transformer = OneHotEncoder(drop='first')
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Combine transformers into a preprocessor with ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Create a pipeline that preprocesses the data and then applies KMeans clustering
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('cluster', KMeans(random_state=42))])

# Fit the pipeline to the data
pipeline.fit(df)

# Determine the optimal number of clusters using the elbow method
inertia = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(pipeline.named_steps['preprocessor'].transform(df))
    inertia.append(kmeans.inertia_)

# Use KneeLocator to find the elbow point
knee_locator = KneeLocator(range(1, 11), inertia, curve='convex', direction='decreasing')
optimal_clusters = knee_locator.elbow

# Refit KMeans with the optimal number of clusters
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
df['Cluster'] = kmeans.fit_predict(pipeline.named_steps['preprocessor'].transform(df))

# Save the clustering results to a CSV file
df.to_csv('/workspace/cluster.csv', index=False, columns=['Cluster'])
print(f"Optimal number of clusters: {optimal_clusters}")
