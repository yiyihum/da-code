import pandas as pd

# Load the training data
train_df = pd.read_csv('/workspace/train.csv')

# Load the additional census data
census_df = pd.read_csv('/workspace/census_starter.csv')

# Explore the training data
print(train_df.describe())
print(train_df.info())

# Check for missing values in the training data
print(train_df.isnull().sum())

# Merge the training data with the census data on the 'cfips' column
train_merged_df = pd.merge(train_df, census_df, on='cfips', how='left')

# Check the merged dataframe
print(train_merged_df.head())

# Save the merged dataframe to a CSV for further analysis
train_merged_df.to_csv('/workspace/train_merged.csv', index=False)
