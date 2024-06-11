import pandas as pd

# Load the datasets again
train = pd.read_csv('/workspace/train.csv')
test = pd.read_csv('/workspace/test.csv')
stores = pd.read_csv('/workspace/stores.csv')
features = pd.read_csv('/workspace/features.csv')

# Merge the train and test datasets with the stores dataset
train_with_stores = pd.merge(train, stores, how='left', on='Store')
test_with_stores = pd.merge(test, stores, how='left', on='Store')

# Merge the train and test datasets with the features dataset
train_with_features = pd.merge(train_with_stores, features, how='left', on=['Store', 'Date'])
test_with_features = pd.merge(test_with_stores, features, how='left', on=['Store', 'Date'])

# Display the first few rows of the merged dataframes
print(train_with_features.head())
print(test_with_features.head())
