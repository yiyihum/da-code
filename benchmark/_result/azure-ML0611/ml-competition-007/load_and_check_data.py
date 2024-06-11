import pandas as pd

# Load the datasets
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Display the first few rows of the train and test datasets
print("Train data shape:", train_data.shape)
print("Test data shape:", test_data.shape)
print("\nFirst 5 rows of train data:")
print(train_data.head())
print("\nFirst 5 rows of test data:")
print(test_data.head())

# Check for missing values in both datasets
print("\nMissing values in train data:")
print(train_data.isnull().sum().sort_values(ascending=False).head(20))
print("\nMissing values in test data:")
print(test_data.isnull().sum().sort_values(ascending=False).head(20))
