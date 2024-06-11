import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Load the dataset with the correct delimiter
df = pd.read_csv('/workspace/marketing_campaign.csv', delimiter='\t')

# Impute missing values in 'Income' with the median
imputer = SimpleImputer(strategy='median')
df['Income'] = imputer.fit_transform(df[['Income']])

# Select columns for one-hot encoding and standard scaling
categorical_features = ['Education', 'Marital_Status']
numerical_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
# Remove non-feature columns and columns with constant values
non_features = ['ID', 'Z_CostContact', 'Z_Revenue']
numerical_features = [feature for feature in numerical_features if feature not in non_features]

# Define the preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])

# Apply the preprocessing pipeline
df_processed = pd.DataFrame(preprocessor.fit_transform(df))
# Get feature names for one-hot encoded columns
one_hot_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features)
feature_names = numerical_features + list(one_hot_feature_names)
df_processed.columns = feature_names

# Display the first few rows of the processed dataset
print(df_processed.head())
