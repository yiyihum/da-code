import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the dataset
df = pd.read_csv('/workspace/property.csv')

# Preprocessing
# Selecting relevant features for clustering
features = df.drop(columns=['item_id', 'district_uuid'])

# Handling boolean columns by converting them to integers
bool_cols = ['has_elevator', 'has_storage_area']
for col in bool_cols:
    features[col] = features[col].fillna(False).astype(int)

# Feature scaling and imputation for numeric features
numeric_features = ['deposit', 'monthly_rent', 'room_qty', 'unit_area', 'building_floor_count', 'unit_floor', 'property_age']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),  # Impute missing values with median
    ('scaler', StandardScaler())
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features)
    ],
    remainder='passthrough'  # Leave boolean features as is
)

# Clustering
kmeans = KMeans(n_clusters=4, random_state=0)
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('clusterer', kmeans)])

# Fit the pipeline to perform clustering
pipeline.fit(features)

# Add cluster labels to the dataframe
df['Cluster'] = pipeline.named_steps['clusterer'].labels_

# Prepare the dataframe for output
processed_features = pipeline.named_steps['preprocessor'].transform(features)
output_df = pd.DataFrame(processed_features, columns=['Processed_Feature_' + str(i) for i in range(processed_features.shape[1])])
output_df['Cluster'] = df['Cluster']

# Save the clustering results to a CSV file
output_df.to_csv('/workspace/cluster.csv', index=False)
