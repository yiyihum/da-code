import pandas as pd
from sklearn.impute import SimpleImputer

# Load the dataset
df = pd.read_csv('/workspace/test.csv')

# Impute missing values for numerical columns with median
num_cols = df.select_dtypes(include=['float64', 'int64']).columns
num_imputer = SimpleImputer(strategy='median')
df[num_cols] = num_imputer.fit_transform(df[num_cols])

# Impute missing values for categorical columns with mode
cat_cols = df.select_dtypes(include=['object']).columns
cat_imputer = SimpleImputer(strategy='most_frequent')
df[cat_cols] = cat_imputer.fit_transform(df[cat_cols])

# Convert 'RainToday' column to binary format
df['RainToday'] = df['RainToday'].map({'Yes': 1, 'No': 0})

# Save the preprocessed data to a new CSV file
df.to_csv('/workspace/preprocessed_test.csv', index=False)

# Print the first few rows of the preprocessed dataframe
print(df.head())
