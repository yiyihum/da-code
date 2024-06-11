import pandas as pd

# Load the datasets
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Display basic information about the datasets
print("Training Data Info:")
print(train_data.info())
print("\nTest Data Info:")
print(test_data.info())

# Check for missing values in the datasets
print("\nMissing Values in Training Data:")
print(train_data.isnull().sum())
print("\nMissing Values in Test Data:")
print(test_data.isnull().sum())

# Display statistical summary of the training data
print("\nStatistical Summary of Training Data:")
print(train_data.describe())

# Check the distribution of the target variable
print("\nDistribution of Target Variable 'Rings':")
print(train_data['Rings'].value_counts())
