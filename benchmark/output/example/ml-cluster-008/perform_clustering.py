import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Load the property data
property_data = pd.read_csv('/workspace/property.csv')

# Drop the identifier columns
property_data.drop(['item_id', 'district_uuid'], axis=1, inplace=True)

# Convert boolean columns to numerical format
property_data['has_elevator'] = property_data['has_elevator'].map({'true': 1, 'false': 0})
property_data['has_storage_area'] = property_data['has_storage_area'].map({'true': 1, 'false': 0})

# Define the preprocessing steps
numeric_features = ['deposit', 'monthly_rent', 'room_qty', 'unit_area', 'building_floor_count', 'unit_floor', 'property_age']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Apply transformations to the numeric features
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features)
    ])

# Define the clustering model
kmeans = KMeans(n_clusters=4, random_state=0)

# Create a pipeline that combines the preprocessor with the clustering model
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('clusterer', kmeans)])

# Fit the pipeline to the property data
pipeline.fit(property_data)

# Predict the cluster labels
property_data['Cluster'] = pipeline.named_steps['clusterer'].labels_

# Save the clustering results to a CSV file
property_data.to_csv('/workspace/cluster.csv', index=False, columns=numeric_features + ['Cluster'])
