import pandas as pd

# Load the datasets
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Display basic information about the datasets
print("Train data shape:", train_data.shape)
print("Test data shape:", test_data.shape)

# Check for missing values in the datasets
print("\nMissing values in train data:")
print(train_data.isnull().sum())
print("\nMissing values in test data:")
print(test_data.isnull().sum())

# Display data types of the features
print("\nData types in train data:")
print(train_data.dtypes)
