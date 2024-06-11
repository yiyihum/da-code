import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Display the first few rows of the training data
print(train_data.head())

# Display the first few rows of the test data
print(test_data.head())

# Display the data types and missing values in the training data
print(train_data.info())

# Display the data types and missing values in the test data
print(test_data.info())
