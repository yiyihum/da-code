import pandas as pd

# Load the datasets
train_data = pd.read_csv('/workspace/New_York_cars.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Display the first few rows of the train and test datasets
print("Train Data:")
print(train_data.head())
print("\nTest Data:")
print(test_data.head())

# Check for missing values in the train and test datasets
print("\nMissing values in Train Data:")
print(train_data.isnull().sum())
print("\nMissing values in Test Data:")
print(test_data.isnull().sum())
