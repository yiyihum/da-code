import pandas as pd

# Load the datasets
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Display the first few rows of the train and test datasets
print("Train Data:")
print(train_data.head())
print("\nTest Data:")
print(test_data.head())

# Display summary statistics of the train dataset
print("\nTrain Data Summary:")
print(train_data.describe())

# Check for missing values in the train and test datasets
print("\nMissing Values in Train Data:")
print(train_data.isnull().sum())
print("\nMissing Values in Test Data:")
print(test_data.isnull().sum())
