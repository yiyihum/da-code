import pandas as pd

# Load the datasets
train_data = pd.read_csv('/workspace/clinvar_conflicting.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Display the first few rows of the training data
print(train_data.head())

# Display the first few rows of the test data
print(test_data.head())

# Display the shape of the datasets
print('Training data shape:', train_data.shape)
print('Test data shape:', test_data.shape)

# Check for missing values in the training data
print('Missing values in training data:')
print(train_data.isnull().sum())

# Check for missing values in the test data
print('Missing values in test data:')
print(test_data.isnull().sum())
