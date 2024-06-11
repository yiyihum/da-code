import pandas as pd

# Load the datasets
features = pd.read_csv('/workspace/features.csv')
stores = pd.read_csv('/workspace/stores.csv')
test = pd.read_csv('/workspace/test.csv')
train = pd.read_csv('/workspace/train.csv')

# Display the first few rows of each dataframe
print(features.head())
print(stores.head())
print(test.head())
print(train.head())
