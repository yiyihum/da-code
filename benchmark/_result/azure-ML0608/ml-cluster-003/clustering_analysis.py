import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Load the dataset
df = pd.read_csv('/workspace/New_York_cars.csv')

# Select a subset of columns for clustering
features = ['money', 'Mileage', 'Year', 'brand', 'Drivetrain', 'Fuel type']

# Preprocessing: Handle missing values and encode categorical variables
numeric_features = ['money', 'Mileage', 'Year']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

categorical_features = ['brand', 'Drivetrain', 'Fuel type']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

# Clustering pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('cluster', KMeans(n_clusters=5, random_state=42))])

# Fit the pipeline to the data
pipeline.fit(df[features])

# Predict the clusters
clusters = pipeline.predict(df[features])

# Add the cluster labels to the dataframe
df['Cluster'] = clusters

# Get the processed features from the pipeline
processed_features = pipeline.named_steps['preprocessor'].transform(df[features])

# Create a DataFrame with the processed features and the cluster labels
# We need to get the correct number of feature names from the transformers
num_features_transformed = list(pipeline.named_steps['preprocessor'].transformers_[0][1].named_steps['scaler'].get_feature_names_out())
cat_features_transformed = list(pipeline.named_steps['preprocessor'].transformers_[1][1].named_steps['onehot'].get_feature_names_out())
all_features_transformed = num_features_transformed + cat_features_transformed

processed_df = pd.DataFrame(processed_features.toarray(), columns=all_features_transformed)
processed_df['Cluster'] = df['Cluster']

# Save the results to a CSV file
processed_df.to_csv('/workspace/cluster.csv', index=False)
