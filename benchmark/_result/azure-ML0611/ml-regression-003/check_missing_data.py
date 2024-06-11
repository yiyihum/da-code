import pandas as pd

# Re-merge the datasets since the previous merged dataframes are not saved as CSV files
train = pd.read_csv('/workspace/train.csv')
test = pd.read_csv('/workspace/test.csv')
stores = pd.read_csv('/workspace/stores.csv')
features = pd.read_csv('/workspace/features.csv')

train_with_stores = pd.merge(train, stores, how='left', on='Store')
test_with_stores = pd.merge(test, stores, how='left', on='Store')
train_with_features = pd.merge(train_with_stores, features, how='left', on=['Store', 'Date'])
test_with_features = pd.merge(test_with_stores, features, how='left', on=['Store', 'Date'])

# Check for missing values and data types
print(train_with_features.info())
print(test_with_features.info())

# Check for any duplicate 'IsHoliday' columns and decide how to handle them
print(train_with_features.columns)
print(test_with_features.columns)
