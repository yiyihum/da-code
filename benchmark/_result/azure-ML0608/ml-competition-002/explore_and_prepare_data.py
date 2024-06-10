import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Display basic information about the dataset
print(train_data.info())
print(train_data.head())

# Check for missing values
print(train_data.isnull().sum())

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Display basic information about the test dataset
print(test_data.info())
print(test_data.head())

# Check for missing values in the test dataset
print(test_data.isnull().sum())
