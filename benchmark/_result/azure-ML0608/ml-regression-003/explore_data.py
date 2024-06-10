import pandas as pd

# Load the datasets
train_df = pd.read_csv('/workspace/train.csv')
test_df = pd.read_csv('/workspace/test.csv')
features_df = pd.read_csv('/workspace/features.csv', na_values=['NA'])
stores_df = pd.read_csv('/workspace/stores.csv')

# Display the first few rows of each dataframe
print("Train DataFrame:")
print(train_df.head())
print("\nTest DataFrame:")
print(test_df.head())
print("\nFeatures DataFrame:")
print(features_df.head())
print("\nStores DataFrame:")
print(stores_df.head())

# Check for missing values
print("\nMissing values in Train DataFrame:")
print(train_df.isnull().sum())
print("\nMissing values in Test DataFrame:")
print(test_df.isnull().sum())
print("\nMissing values in Features DataFrame:")
print(features_df.isnull().sum())
print("\nMissing values in Stores DataFrame:")
print(stores_df.isnull().sum())

# Basic statistics of numerical features
print("\nStatistics of Train DataFrame:")
print(train_df.describe())
print("\nStatistics of Features DataFrame:")
print(features_df.describe())
print("\nStatistics of Stores DataFrame:")
print(stores_df.describe())
