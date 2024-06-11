import pandas as pd

# Load the datasets
train_df = pd.read_csv('/workspace/top_10000_1960-now.csv')
test_df = pd.read_csv('/workspace/test.csv')

# Display the first few rows of the training data
print("Training Data:")
print(train_df.head())

# Display the first few rows of the test data
print("\nTest Data:")
print(test_df.head())

# Check for missing values in the training data
print("\nMissing values in training data:")
print(train_df.isnull().sum())

# Check for missing values in the test data
print("\nMissing values in test data:")
print(test_df.isnull().sum())
