import pandas as pd

# Load the datasets
postings_df = pd.read_csv('/workspace/postings.csv')
test_df = pd.read_csv('/workspace/test.csv')

# Display the first few rows of the postings dataframe
print(postings_df.head())

# Display the first few rows of the test dataframe
print(test_df.head())

# Check for missing values in the target column of the postings dataframe
print(postings_df['formatted_experience_level'].isnull().sum())

# Get a summary of the postings dataframe
print(postings_df.describe(include='all'))

# Get a summary of the test dataframe
print(test_df.describe(include='all'))
