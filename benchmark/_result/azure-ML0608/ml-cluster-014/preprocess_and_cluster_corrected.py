import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the dataset with the correct delimiter
data = pd.read_csv('/workspace/marketing_campaign.csv', delimiter='\t')

# Drop columns that are not useful for clustering
data.drop(['ID', 'Z_CostContact', 'Z_Revenue'], axis=1, inplace=True)

# Handle missing values by imputing with the median
imputer = SimpleImputer(strategy='median')
data['Income'] = imputer.fit_transform(data[['Income']])

# Convert 'Dt_Customer' to a numerical feature by calculating the number of days since the customer joined
data['Dt_Customer'] = pd.to_datetime(data['Dt_Customer'], format='%d-%m-%Y')
data['Days_Enrolled'] = (pd.to_datetime("now") - data['Dt_Customer']).dt.days
data.drop('Dt_Customer', axis=1, inplace=True)

# Select categorical columns
categorical_cols = data.select_dtypes(include=['object']).columns

# Apply one-hot encoding to categorical columns
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ],
    remainder='passthrough'
)

# Create a preprocessing and clustering pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('scaler', StandardScaler()),
    ('cluster', KMeans(n_clusters=5, random_state=42))
])

# Fit the pipeline to the data
pipeline.fit(data)

# Predict the clusters
clusters = pipeline.predict(data)

# Add the cluster labels to the original data
data['Cluster'] = clusters

# Select only the processed features and the cluster label
processed_features = pipeline.named_steps['preprocessor'].transform(data)
processed_feature_names = pipeline.named_steps['preprocessor'].get_feature_names_out()
processed_data = pd.DataFrame(processed_features, columns=processed_feature_names)
processed_data['Cluster'] = data['Cluster']

# Save the processed data and clusters to a CSV file
processed_data.to_csv('/workspace/cluster.csv', index=False)
